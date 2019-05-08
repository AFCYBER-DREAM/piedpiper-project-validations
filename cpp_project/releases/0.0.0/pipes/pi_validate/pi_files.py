from marshmallow import fields
from marshmallow import Schema
from marshmallow import RAISE
from marshmallow import ValidationError
from marshmallow import validates


class FileVars(Schema):
    file = fields.Str(required=True)
    styler = fields.Str(required=True)
    sast = fields.Str(required=True)

    @validates('styler')
    def validate_styler(self, value):
        allowed_stylers = [
            'noop',
            'cpplint',
            'flake8',
        ]

        errors = []
        if value not in allowed_stylers:
            errors.append(ValueError(f'File styler must be one of {allowed_stylers}. You passed {value}'))
        if len(errors):
            raise ValidationError(errors)

    @validates('sast')
    def validate_sast(self, value):
        allowed_sast = [
            'noop',
            'cppcheck',
            'pybandit',
        ]

        errors = []
        if value not in allowed_sast:
            errors.append(ValueError(f'File sast must be one of {allowed_sast}. You passed {value}'))
        if len(errors):
            raise ValidationError(errors)


class FileConfig(Schema):
    file_config = fields.List(fields.Nested(FileVars), many=True)


def validate(config):
    schema = FileConfig(unknown=RAISE)
    try:
       _ = schema.load(config)
       result = True
    except ValidationError as err:
        result = err
    return result
