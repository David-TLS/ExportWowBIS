from tools import Classe, Item, Phase, Spe

classes = [
    classes("warrior", [Spe("prot"), Spe("fury")]),
    classes("warlock", [Spe("all")]),
    classes("shaman", [Spe("elem"), Spe("resto"), Spe("enhan")]),
    classes("rogue", [Spe("dagger"), Spe("sword")]),
    classes("priest", [Spe("holy"), Spe("shadow")]),
    classes("paladin", [Spe("ret"), Spe("protection"), Spe("heal")]),
    classes("mage", [Spe("all")]),
    classes("druid", [Spe("tank"), Spe("balance"), Spe("cat"), Spe("resto")]),
]

phase = [
    Phase("3", classes),
    Phase("4", classes),
    Phase("5", classes),
    Phase("6", classes)
]
