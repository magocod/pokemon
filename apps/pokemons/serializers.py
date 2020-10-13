from rest_framework import serializers

from apps.pokemons.models import (
    Captured,
    Move,
    NameStatistic,
    Specie,
    Sprite,
    Statistic,
)

from .exceptions import ActivePokemonLimitReached


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


class CapturedBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Captured
        fields = ("id", "nick_name", "is_party_member", "specie")


class CapturedEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Captured
        fields = ("nick_name",)

    def update(self, instance, validated_data):
        """
        ...
        """

        instance.nick_name = validated_data.get("nick_name", instance.nick_name)
        instance.save()
        return CapturedBasicSerializer(instance).data


class CapturedCreateSerializer(serializers.Serializer):
    """
    create by checking the limit number
    of active members per user
    """

    nick_name = serializers.CharField(max_length=80)
    is_party_member = serializers.BooleanField()
    specie = serializers.IntegerField()

    def validate_specie(self, value):
        """
        ...
        """
        try:
            Specie.objects.get(pk=value)
            return value
        except Specie.DoesNotExist:
            raise serializers.ValidationError("species does not exist")

    def create(self, validated_data):
        user = self.context["request"].user

        instance = Captured(
            nick_name=validated_data["nick_name"],
            is_party_member=validated_data["is_party_member"],
            specie_id=validated_data["specie"],
            user_id=user.id,
        )

        if validated_data["is_party_member"]:
            party_member_count = Captured.objects.filter(
                is_party_member=True, user_id=user.id
            ).count()
            # print(party_member_count)

            if party_member_count <= Captured.active_member_limit():
                instance.is_party_member = False

        instance.save()

        return CapturedBasicSerializer(instance).data


class CapturedSerializer(serializers.ModelSerializer):

    specie = SpecieBasicSerializer(many=False)

    class Meta:
        model = Captured
        fields = ("id", "nick_name", "is_party_member", "specie")


class SwapPartyMemberSerializer(serializers.Serializer):
    """
    trade, add, or remove a user's active Pokémon

    Before making an exchange check if it exists
    or the pokemon belongs to the user
    """

    entering_the_party = serializers.IntegerField(required=False, allow_null=True)
    leaving_the_party = serializers.IntegerField(required=False, allow_null=True)


    def validate_entering_the_party(self, value):
        """

        Arguments:
            value {[type]} -- [description]

        Returns:
            [tuple] -- [value, captured]

        Raises:
            serializers -- [description]
        """
        if value is None:
            return value
        try:
            captured = Captured.objects.get(pk=value)
        except Captured.DoesNotExist:
            raise serializers.ValidationError("pokemon to exchange does not exist")

        user_id: int = self.context["user_id"]
        if captured.user_id != user_id:
            raise serializers.ValidationError("this pokemon is not in user storage")

        return value, captured

    def validate_leaving_the_party(self, value):
        """

        Arguments:
            value {int | str} -- [description]

        Returns:
            [tuple] -- [value, captured]

        Raises:
            serializers -- [description]
        """
        if value is None:
            return value
        try:
            captured = Captured.objects.get(pk=value)
        except Captured.DoesNotExist:
            raise serializers.ValidationError("pokemon to exchange does not exist")

        user_id: int = self.context["user_id"]
        if captured.user_id != user_id:
            raise serializers.ValidationError("this pokemon is not in user storage")

        return value, captured

    def create(self, validated_data):
        user_id: int = self.context["user_id"]

        if validated_data["leaving_the_party"] is not None:
            _, captured_leaving = validated_data["leaving_the_party"]
            # print("leaving", _, captured_leaving)

            if captured_leaving.is_party_member:
                captured_leaving.is_party_member = False
                captured_leaving.save()

        if validated_data["entering_the_party"] is not None:
            _, captured_entering = validated_data["entering_the_party"]
            # print("entering", _, captured_entering)

            if not captured_entering.is_party_member:
                # check how many active pokémon there are
                current_team_count = Captured.objects.filter(
                    is_party_member=True,
                    user_id=user_id
                ).count()
                if current_team_count < Captured.active_member_limit():
                    captured_entering.is_party_member = True
                    captured_entering.save()
                else:
                    raise ActivePokemonLimitReached

        # return the user's current pokemon team, serialized
        serializer_team = CapturedSerializer(
            Captured.objects.filter(
                is_party_member=True,
                user_id=user_id
            ),
            many=True
        )
        return serializer_team.data
