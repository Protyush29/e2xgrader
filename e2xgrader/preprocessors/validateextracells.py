import traceback

from nbgrader.nbgraderformat import ValidationError
from nbgrader.preprocessors import NbGraderPreprocessor

class ExtraCellValidator:

    def validate_cell(self, cell):

        if 'nbgrader' not in cell.metadata:
            return

        meta = cell.metadata['nbgrader']
        grade = meta['grade']
        solution = meta['solution']
        locked = meta['locked']
        task = meta.get('task', False)

        # check if there is a single choice cell without a solution
        if is_singlechoice(cell):
            extended_metadata = cell.metadata.extended_cell
            if (not 'choice' in extended_metadata) or (len(extended_metadata.choice) < 1):
                raise ValidationError("single choice nbgrader cell {} does not have a solution".format(cell.metadata.nbgrader.grade_id))

    def validate_nb(self, nb):
        ids = set([])
        for cell in nb.cells:
            self.validate_cell(cell)

class ValidateExtraCells(NbGraderPreprocessor):
    """A preprocessor for checking that choice cells have valid solutions."""

    def preprocess(self, nb, resources):
        try:
            ExtraCellValidator().validate_nb(nb)
        except ValidationError:
            self.log.error(traceback.format_exc())
            msg = "Some choice cells seem to miss a solution. Please check them again."
            self.log.error(msg)
            raise ValidationError(msg)

        return nb, resources