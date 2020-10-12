from rest_framework import serializers

from apps.pokemons.models import Move, NameStatistic, Specie, Sprite, Statistic


class NameStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = NameStatistic
        fields = ["name"]


class NameStatisticField(serializers.RelatedField):
    def to_representation(self, value):
        return value.name


class StatisticSerializer(serializers.ModelSerializer):

    name = NameStatisticField(read_only=True)

    class Meta:
        model = Statistic
        fields = ["name", "value"]


class SpriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprite
        fields = [
            "back_default",
            "back_female",
            "back_shiny",
            "back_shiny_female",
            "front_default",
            "front_female",
            "front_shiny",
            "front_shiny_female",
        ]


class MoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Move
        fields = ["name"]


class SpecieBasicSerializer(serializers.ModelSerializer):

    sprites = SpriteSerializer(many=False)

    class Meta:
        model = Specie
        fields = (
            "id",
            "name",
            # relations
            "sprites",
        )


class SpecieSerializer(serializers.ModelSerializer):
    """
    ...
    """

    stats = StatisticSerializer(many=True)
    sprites = SpriteSerializer(many=False)
    # moves = MoveSerializer(many=True)
    moves = serializers.StringRelatedField(many=True)
    abilities = serializers.StringRelatedField(many=True)
    types = serializers.StringRelatedField(many=True)

    class Meta:
        model = Specie
        fields = (
            "id",
            "capture_rate",
            "color",
            "flavor_text",
            "height",
            "name",
            "weight",
            # relations
            "stats",
            "sprites",
            "moves",
            "abilities",
            "types",
        )
