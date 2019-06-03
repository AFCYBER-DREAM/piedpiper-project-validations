from marshmallow import fields
from marshmallow import Schema
from marshmallow import RAISE
from marshmallow import INCLUDE
from marshmallow import ValidationError
from marshmallow import validates
from marshmallow import pre_load

class Stage(Schema):
    name = fields.Str(required=True)
    deps = fields.List(fields.Str(), required=True, allow_none=True)
    resources = fields.List(fields.Dict())


class ValidateStageConfig(Schema):
    resource = fields.Str(required=True)
    policy_version = fields.Str(required=True)

class StyleStageConfig(Schema):
    files = fields.Str(required=True)
    resource = fields.Str(required=True)

    @validates('resource')
    def validate_style_config_resource(self, value):
        if value != 'flake8':
            raise ValidationError(f"Resource must be flake8. You provided {value}")


class ValidateStage(Stage):
    config = fields.List(fields.Nested(ValidateStageConfig))

class StyleStage(Stage):
    resources = fields.List(fields.Dict())
    config = fields.List(fields.Nested(StyleStageConfig, unknown=INCLUDE))

    @validates('resources')
    def validate_style_resources(self, value):
        if {'name': 'flake8', 'uri': '/function/piedpiper-flake8-gateway'} not in value:
            raise ValidationError(f"Resource config is invalid for Style Stage. {value}")



def validate(stages):
    results = []
    for stage in stages:
        stage_name = stage.get('name')
        if stage_name == 'validate':
            schema = ValidateStage()
        elif stage_name == 'style':
            schema = StyleStage()
        else:
            continue
        try:
            _ = schema.load(stage)
            results.append(True)
        except ValidationError as err:
            result.append(err)
    return results
