def parbaudi_registracijas_datus(vards, uzvards, lietotajvards):
    kludas = []
    if not vards or vards.isspace():
        kludas.append("Vārds ir obligāts!")
    if not uzvards or uzvards.isspace():
        kludas.append("Uzvārds ir obligāts!")
    if not lietotajvards or lietotajvards.isspace():
        kludas.append("Lietotājvārds ir obligāts!")
    return kludas

def parbaudi_zinojuma_datus(teksts, lietotajs_id):
    kludas = []
    if not teksts or teksts.isspace():
        kludas.append("Ziņojuma teksts ir obligāts!")
    if not lietotajs_id:
        kludas.append("Jāizvēlas lietotājs!")
    return kludas 