class Prestiges:
    def __init__(self):
        self.stone = Role(396837260378505216, "⭐")
        self.iron = Role(396837540612800544, "🌟")
        self.gold = Role(396837663660834827, "✨")
        self.diamond = Role(396837745097441280, "💫")
        self.emerald = Role(406150428947120159, "☄")
        self.sapphire = Role(428317168728276992, "")
        self.ruby = Role(428317393236787200, "✵")
        self.crystal = Role(439863000988647425, "✫")
        self.opal = Role(452908345133629440, "✰")
        self.amethyst = Role(467524155349139456, "✯")
        self.rainbow = Role(479478482171068420, "🌈")

        self.prime = Prime()

        self.mirror = Role(763979582994513940, "✬")
        self.light = Role(802232852401487912, "✬")
        self.dawn = Role(802233176306352159, "✬")
        self.dusk = Role(802233180584149058, "✬")
        self.air = Role(802233186586198086, "✬")
        self.wind = Role(802233192148107395, "✬")
        self.nebula = Role(802233234384486440, "✬")
        self.thunder = Role(802233547469226015, "✬")
        self.earth = Role(802236219764506695, "✬")
        self.water = Role(802236232876687391, "✬")
        self.fire = Role(802236235388026913, "✬")

        self.all = [
            self.stone,
            self.iron,
            self.gold,
            self.diamond,
            self.emerald,
            self.sapphire,
            self.ruby,
            self.crystal,
            self.opal,
            self.amethyst,
            self.rainbow,
            self.prime.iron,
            self.prime.gold,
            self.prime.diamond,
            self.prime.emerald,
            self.prime.sapphire,
            self.prime.ruby,
            self.prime.crystal,
            self.prime.opal,
            self.prime.amethyst,
            self.mirror,
            self.light,
            self.dawn,
            self.dusk,
            self.air,
            self.wind,
            self.nebula,
            self.thunder,
            self.earth,
            self.water,
            self.fire
        ]


class Prime:
    def __init__(self):
        self.iron = Role(763977262601076756, "✪")
        self.gold = Role(763977448768536606, "✪")
        self.diamond = Role(763977567035195462, "✪")
        self.emerald = Role(763977687903109160, "✪")
        self.sapphire = Role(763978311733870602, "✪")
        self.ruby = Role(763978476348637195, "✪")
        self.crystal = Role(763978613082554389, "✪")
        self.opal = Role(763978744334909440, "✪")
        self.amethyst = Role(763979533212188703, "✪")


class Role:
    def __init__(self, id_, star):
        self.id = id_
        self.star = star
        self.role = None

    def get(self, guild):
        self.role = guild.get_role(self.id)
