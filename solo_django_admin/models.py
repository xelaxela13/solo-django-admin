from typing import Any, Dict, List, Optional, Union

from django.db import models
from tortoise import Model as TortoiseModel
from tortoise.fields.base import OnDelete

COMMON_PARAMS: List[str] = [
    'default',
    'null',
    'unique',
    'primary_key',
    'editable',
]

FIELD_MAPPING: Dict[str, Dict[str, Union[models.Field, List[str]]]] = {
    'CharField': {
        'field_class': models.CharField,
        'params': ['max_length', *COMMON_PARAMS],
    },
    'CharEnumFieldInstance': {
        'field_class': models.CharField,
        'params': ['choices', *COMMON_PARAMS],
    },
    'BooleanField': {
        'field_class': models.BooleanField,
        'params': COMMON_PARAMS
    },
    'DateField': {
        'field_class': models.DateField,
        'params': ['auto_now_add', 'auto_now', *COMMON_PARAMS]
    },
    'DatetimeField': {
        'field_class': models.DateTimeField,
        'params': ['auto_now_add', 'auto_now', *COMMON_PARAMS]
    },
    'DurationField': {
        'field_class': models.DurationField,
        'params': COMMON_PARAMS
    },
    'DecimalField': {
        'field_class': models.DecimalField,
        'params': ['max_digits', 'decimal_places', *COMMON_PARAMS]
    },
    'EmailField': {
        'field_class': models.EmailField,
        'params': COMMON_PARAMS
    },
    'FileField': {
        'field_class': models.FileField,
        'params': ['max_length', *COMMON_PARAMS]
    },
    'URLField': {
        'field_class': models.URLField,
        'params': ['max_length', *COMMON_PARAMS]
    },
    'UUIDField': {
        'field_class': models.UUIDField,
        'params': ['max_length', *COMMON_PARAMS]
    },
    'IntegerField': {
        'field_class': models.IntegerField,
        'params': ['min_value', 'max_value', *COMMON_PARAMS]
    },
    'IntEnumFieldInstance': {
        'field_class': models.IntegerField,
        'params': ['choices', *COMMON_PARAMS]
    },
    'SmallIntField': {
        'field_class': models.SmallIntegerField,
        'params': ['min_value', 'max_value', *COMMON_PARAMS]
    },
    'BigIntField': {
        'field_class': models.BigIntegerField,
        'params': ['min_value', 'max_value', *COMMON_PARAMS]
    },
    'PositiveIntegerField': {
        'field_class': models.PositiveIntegerField,
        'params': ['min_value', 'max_value', *COMMON_PARAMS]
    },
    'PositiveSmallIntegerField': {
        'field_class': models.PositiveSmallIntegerField,
        'params': ['min_value', 'max_value', *COMMON_PARAMS]
    },
    'SlugField': {
        'field_class': models.SlugField,
        'params': COMMON_PARAMS
    },
    'FloatField': {
        'field_class': models.FloatField,
        'params': COMMON_PARAMS
    },
    'JSONField': {
        'field_class': models.JSONField,
        'params': COMMON_PARAMS
    },
    'BinaryField': {
        'field_class': models.BinaryField,
        'params': ['max_length', *COMMON_PARAMS]
    },
    'ForeignKeyFieldInstance': {
        'field_class': models.ForeignKey,
        'params': [
            'db_index',
            'related_name',
            'on_delete',
            'to_field',
            'db_constraint',
            'to',
            *COMMON_PARAMS
        ]
    },
    'OneToOneFieldInstance': {
        'field_class': models.OneToOneField,
        'params': [
            'db_index',
            'related_name',
            'on_delete',
            'to_field',
            'db_constraint',
            'to',
            *COMMON_PARAMS
        ]
    },
    'ManyToManyFieldInstance': {
        'field_class': models.ManyToManyField,
        'params': [
            'related_name',
            'through',
            'db_constraint',
            'to',
            'db_table',
            *COMMON_PARAMS
        ]
    },
}

FK_ON_DELETE_MAPPER: Dict[OnDelete, models.deletion.CASCADE] = {
    OnDelete.CASCADE: models.CASCADE,
    OnDelete.SET_NULL: models.SET_NULL,
    OnDelete.RESTRICT: models.RESTRICT,
    OnDelete.NO_ACTION: models.DO_NOTHING,
    OnDelete.SET_DEFAULT: models.SET_DEFAULT,
}


class MapperMeta(models.base.ModelBase):
    def __new__(
            cls,
            name: str,
            bases: tuple,
            attrs: dict
    ) -> 'MapperModel':
        fast_api_model: Optional[TortoiseModel] = attrs.get(
            'fast_api_model',
            None
        )
        if not fast_api_model:
            return super().__new__(cls, name, bases, attrs)

        assert fast_api_model is not None and issubclass(fast_api_model, TortoiseModel), "fast_api_model is required and must be TortoiseModel class"  # noqa

        tortoise_fields = fast_api_model._meta.fields_map
        for field_name, field_info in tortoise_fields.items():
            field_type: str = field_info.__class__.__name__
            try:
                field_class = FIELD_MAPPING[field_type]['field_class']
                params = FIELD_MAPPING[field_type]['params']
            except KeyError:
                continue

            try:
                attrs[field_name]
            except KeyError:
                exists_params: Dict[str, Any] = {}
                for param in params:
                    exist_param = cls.map_param(
                        param,
                        field_name,
                        field_info,
                        field_type,
                        attrs
                    )
                    if exist_param is not None:
                        exists_params[param] = exist_param
                attrs[field_name] = field_class(**exists_params)

        new_class = super().__new__(cls, name, bases, attrs)

        base_meta = getattr(new_class, "_meta", None)
        base_meta.db_table = cls.get_db_table_name(new_class)
        base_meta.managed = False
        if not hasattr(new_class, 'id'):
            new_class.add_to_class('id', models.AutoField())
        return new_class

    @classmethod
    def get_db_table_name(
            cls,
            new_class: type
    ) -> str:
        auto_db_table: bool = new_class.auto_db_table
        db_table: str = new_class._meta.db_table
        if auto_db_table:
            db_table = new_class.fast_api_model._meta.db_table or new_class.__name__.lower()  # noqa
        return db_table

    @classmethod
    def get_many_to_many_db_table(
            cls,
            attrs: Dict[str, Any],
            field_info: Any
    ) -> str:
        model_field_name = field_info.__dict__.get('model_field_name')
        model_name = field_info.__dict__.get('model_name')
        if model_field_name:
            return attrs.get(f"{model_field_name}_db_table".lower())
        elif model_name:
            model_name = model_name.split('.')[-1]
            return attrs.get(f"{model_name}_db_table".lower())
        raise ValueError(f"{model_field_name or model_name}_db_table not implemented error")  # noqa

    @classmethod
    def map_param(
            cls,
            param: str,
            field_name: str,
            field_info: Any,
            field_type: str,
            attrs: dict
    ) -> Optional[Any]:
        is_many_to_many_field: bool = field_type == 'ManyToManyFieldInstance'
        param = {
            'primary_key': 'pk',
            'db_index': 'index',
        }.get(param, param)
        if param == 'editable' and field_name == 'id':
            return False
        if param == 'on_delete':
            return FK_ON_DELETE_MAPPER[field_info.__dict__.get(param)]
        if param == 'to':
            return cls.get_related_model(attrs, field_info)
        if param == 'db_table' and is_many_to_many_field:
            return cls.get_many_to_many_db_table(attrs, field_info)
        if param == 'choices':
            return [(i.value, i.name) for i in
                    field_info.__dict__.get('enum_type')]
        return field_info.__dict__.get(param)

    @classmethod
    def get_related_model(
            cls, attrs:
            Dict[str, Any],
            field_info: Any
    ) -> str:
        model_field_name = field_info.__dict__.get('model_field_name')
        model_name = field_info.__dict__.get('model_name')
        if model_field_name:
            return attrs.get(f"{model_field_name}_related_path".lower())
        elif model_name:
            model_name = model_name.split('.')[-1]
            return attrs.get(f"{model_name}_related_path".lower())
        raise ValueError(f"{model_field_name or model_name}_related_path not implemented error")  # noqa


class MapperModel(models.Model, metaclass=MapperMeta):
    fast_api_model: Optional[TortoiseModel] = None
    auto_db_table: bool = True
    MODEL_related_path: Optional[str] = None
    MODEL_db_table: Optional[str] = None

    class Meta:
        abstract: bool = True
        managed: bool = False
