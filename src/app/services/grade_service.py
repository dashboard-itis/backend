import csv
from io import BytesIO, StringIO
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import BadZipFile, ZipFile

from app.dependencies.repositories import GradeRepositoryDep
from app.models.grade import GradeCreate, GradePublic, GradeUpdate
from app.schemas.base import PaginatedResponse
from app.schemas.grade import (
    GradeExportItem,
    GradeImportError,
    GradeImportResult,
    StudentGradeResponse,
)

MIN_SCORE = 0
MAX_SCORE = 100
REQUIRED_IMPORT_COLUMNS = {'student_email', 'course_name', 'score'}
SUPPORTED_IMPORT_EXTENSIONS = {'.csv', '.xlsx'}


class GradeService:
    def __init__(self, grade_repo: GradeRepositoryDep):
        self.grade_repo = grade_repo

    def _to_student_grade_response(self, grade) -> StudentGradeResponse:
        course = grade.course

        return StudentGradeResponse(
            id=grade.id,
            student_id=grade.student_id,
            course_id=grade.course_id,
            score=grade.score,
            comment=grade.comment,
            created_at=grade.created_at,
            updated_at=grade.updated_at,
            course_name=course.name if course else None,
        )

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> PaginatedResponse[StudentGradeResponse]:
        total = await self.grade_repo.count()
        grades = await self.grade_repo.fetch_with_relations(skip=skip, limit=limit)

        return PaginatedResponse[StudentGradeResponse](
            items=[self._to_student_grade_response(grade) for grade in grades],
            total=total,
            skip=skip,
            limit=limit,
        )

    async def get_by_id(self, grade_id: int) -> StudentGradeResponse | None:
        grade = await self.grade_repo.get_with_relations(grade_id)
        return self._to_student_grade_response(grade) if grade else None

    async def create(self, grade_data: GradeCreate) -> GradePublic:
        await self._validate_references(
            student_id=grade_data.student_id,
            course_id=grade_data.course_id,
        )
        grade = await self.grade_repo.create(**grade_data.model_dump())
        return GradePublic.model_validate(grade)

    async def import_from_file(
        self,
        content: bytes,
        filename: str,
    ) -> GradeImportResult:
        rows = self._parse_import_file(content=content, filename=filename)
        errors: list[GradeImportError] = []
        created = 0

        for row_number, row in rows:
            try:
                grade_data = await self._build_import_grade(row)
                await self.create(grade_data)
            except ValueError as exc:
                errors.append(GradeImportError(row=row_number, message=str(exc)))
                continue

            created += 1

        return GradeImportResult(
            created=created,
            failed=len(errors),
            errors=errors,
        )

    async def export_to_json(
        self,
        student_id: int | None = None,
        course_id: int | None = None,
        group_id: int | None = None,
    ) -> list[GradeExportItem]:
        rows = await self.grade_repo.fetch_export_rows(
            student_id=student_id,
            course_id=course_id,
            group_id=group_id,
        )

        return [
            GradeExportItem(
                student_email=student_email,
                student_last_name=student_last_name,
                student_first_name=student_first_name,
                group_id=group_id,
                group_name=group_name,
                course_name=course_name,
                score=score,
                comment=comment,
            )
            for (
                student_email,
                student_last_name,
                student_first_name,
                group_id,
                group_name,
                course_name,
                score,
                comment,
            ) in rows
        ]

    async def update(
        self,
        grade_id: int,
        grade_data: GradeUpdate,
    ) -> GradePublic | None:
        existing = await self.grade_repo.get(grade_id)

        if existing is None:
            return None

        update_data = grade_data.model_dump(exclude_unset=True)
        await self._validate_references(
            student_id=update_data.get('student_id'),
            course_id=update_data.get('course_id'),
        )

        grade = await self.grade_repo.update(grade_id, **update_data)
        return GradePublic.model_validate(grade) if grade else None

    async def delete(self, grade_id: int) -> bool:
        grade = await self.grade_repo.delete(grade_id)
        return grade is not None

    async def get_student_grades(
        self,
        student_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> PaginatedResponse[StudentGradeResponse]:
        total = await self.grade_repo.count(filters={'student_id': student_id})
        grades = await self.grade_repo.get_student_grades_with_course(
            student_id=student_id,
            skip=skip,
            limit=limit,
        )

        return PaginatedResponse[StudentGradeResponse](
            items=[self._to_student_grade_response(grade) for grade in grades],
            total=total,
            skip=skip,
            limit=limit,
        )

    async def _validate_references(
        self,
        student_id: int | None = None,
        course_id: int | None = None,
    ) -> None:
        if student_id is not None and not await self.grade_repo.student_exists(
            student_id
        ):
            raise ValueError('Student not found')

        if course_id is not None and not await self.grade_repo.course_exists(course_id):
            raise ValueError('Course not found')

    async def _build_import_grade(self, row: dict[str, str]) -> GradeCreate:
        student_email = self._required_value(row, 'student_email')
        course_name = self._required_value(row, 'course_name')
        score = self._parse_score(self._required_value(row, 'score'))
        comment = row.get('comment') or None

        student_id = await self.grade_repo.get_student_id_by_email(student_email)
        if student_id is None:
            raise ValueError(f'Student with email "{student_email}" not found')

        course_id = await self.grade_repo.get_course_id_by_name(course_name)
        if course_id is None:
            raise ValueError(f'Course "{course_name}" not found')

        return GradeCreate(
            student_id=student_id,
            course_id=course_id,
            score=score,
            comment=comment,
        )

    def _parse_import_file(
        self,
        content: bytes,
        filename: str,
    ) -> list[tuple[int, dict[str, str]]]:
        extension = Path(filename).suffix.lower()

        if extension not in SUPPORTED_IMPORT_EXTENSIONS:
            raise ValueError('Only .csv and .xlsx files are supported')

        if extension == '.csv':
            rows = self._parse_csv(content)
        else:
            rows = self._parse_xlsx(content)

        if not rows:
            raise ValueError('Import file is empty')

        self._validate_import_columns(rows[0][1])
        return rows

    def _parse_csv(self, content: bytes) -> list[tuple[int, dict[str, str]]]:
        text = content.decode('utf-8-sig')
        sample = text[:1024]
        dialect = csv.Sniffer().sniff(sample, delimiters=',;\t')
        reader = csv.DictReader(StringIO(text), dialect=dialect)

        return [
            (index, self._normalize_row(row))
            for index, row in enumerate(reader, start=2)
            if self._has_values(row)
        ]

    def _parse_xlsx(self, content: bytes) -> list[tuple[int, dict[str, str]]]:
        try:
            with ZipFile(BytesIO(content)) as archive:
                shared_strings = self._read_shared_strings(archive)
                sheet_xml = archive.read('xl/worksheets/sheet1.xml')
        except (BadZipFile, KeyError) as exc:
            raise ValueError('Invalid .xlsx file') from exc

        try:
            raw_rows = self._read_xlsx_rows(sheet_xml, shared_strings)
        except ET.ParseError as exc:
            raise ValueError('Invalid .xlsx file') from exc
        if not raw_rows:
            return []

        headers = [self._normalize_cell(value) for value in raw_rows[0]]
        rows: list[tuple[int, dict[str, str]]] = []

        for row_number, values in enumerate(raw_rows[1:], start=2):
            row = {
                header: self._normalize_cell(values[index])
                for index, header in enumerate(headers)
                if header and index < len(values)
            }

            if self._has_values(row):
                rows.append((row_number, row))

        return rows

    def _read_shared_strings(self, archive: ZipFile) -> list[str]:
        try:
            shared_xml = archive.read('xl/sharedStrings.xml')
        except KeyError:
            return []

        root = ET.fromstring(shared_xml)
        strings: list[str] = []

        for item in root:
            strings.append(''.join(node.text or '' for node in item.iter()))

        return strings

    def _read_xlsx_rows(
        self,
        sheet_xml: bytes,
        shared_strings: list[str],
    ) -> list[list[str]]:
        root = ET.fromstring(sheet_xml)
        rows: list[list[str]] = []

        for row in root.iter():
            if self._strip_namespace(row.tag) != 'row':
                continue

            values: list[str] = []
            for cell in row:
                if self._strip_namespace(cell.tag) != 'c':
                    continue

                column_index = self._cell_column_index(cell.attrib.get('r', ''))
                while len(values) <= column_index:
                    values.append('')

                values[column_index] = self._read_xlsx_cell(cell, shared_strings)

            rows.append(values)

        return rows

    def _read_xlsx_cell(self, cell, shared_strings: list[str]) -> str:
        cell_type = cell.attrib.get('t')

        if cell_type == 'inlineStr':
            return ''.join(node.text or '' for node in cell.iter())

        value_node = next(
            (
                child
                for child in cell
                if self._strip_namespace(child.tag) == 'v'
            ),
            None,
        )

        if value_node is None or value_node.text is None:
            return ''

        if cell_type == 's':
            return shared_strings[int(value_node.text)]

        return value_node.text

    def _validate_import_columns(self, row: dict[str, str]) -> None:
        missing_columns = REQUIRED_IMPORT_COLUMNS - set(row)

        if missing_columns:
            columns = ', '.join(sorted(missing_columns))
            raise ValueError(f'Missing required columns: {columns}')

    def _required_value(self, row: dict[str, str], field_name: str) -> str:
        value = self._normalize_cell(row.get(field_name, ''))

        if not value:
            raise ValueError(f'Column "{field_name}" is required')

        return value

    def _parse_score(self, raw_score: str) -> float:
        try:
            score = float(raw_score.replace(',', '.'))
        except ValueError as exc:
            raise ValueError('Score must be a number') from exc

        if score < MIN_SCORE or score > MAX_SCORE:
            raise ValueError('Score must be between 0 and 100')

        return score

    def _normalize_row(self, row: dict[str, str | None]) -> dict[str, str]:
        return {
            self._normalize_cell(key): self._normalize_cell(value)
            for key, value in row.items()
            if key is not None
        }

    def _normalize_cell(self, value: str | None) -> str:
        return (value or '').strip()

    def _has_values(self, row: dict) -> bool:
        return any(self._normalize_cell(value) for value in row.values())

    def _strip_namespace(self, tag: str) -> str:
        return tag.rsplit('}', maxsplit=1)[-1]

    def _cell_column_index(self, cell_reference: str) -> int:
        letters = ''.join(char for char in cell_reference if char.isalpha())
        index = 0

        for char in letters:
            index = index * 26 + ord(char.upper()) - ord('A') + 1

        return max(index - 1, 0)
