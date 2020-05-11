from os import listdir
import matplotlib.pyplot as plt

def encontrar_curso_crn(crn):
    codigo = ""
    for curso in cursos:
        if curso["crn"]==crn:
            codigo = curso["codigo"]
            break
    return codigo
def load_cursos():
    f = open("../docs/iyr.csv")
    lines = f.readlines()
    info_retiros = []
    lines = lines[1:]
    for line in lines:
        datos = line.split(";")

        periodo = datos[0]
        codigo = datos[1]
        crn = datos[2]
        retiros = datos[3].split('"')[1]
        inscritos = datos[4].rstrip()

        info_retiros.append({"periodo":periodo,
                             "codigo":codigo,
                             "crn":crn,
                             "retiros":retiros,
                             "inscritos":inscritos})
    f.close()
    return info_retiros

def load_notas():
    f = open("../docs/nota.csv")
    lines = f.readlines()
    info_notas = []
    print(lines[0])
    lines = lines[1:]

    for line in lines:
        datos = line.split(";")

        periodo = datos[0]
        subperiodo = datos[1]
        codigo = datos[2]
        crn = datos[3]
        login = datos[4]
        nota = datos[5]
        semestre = datos[6]
        promedio = datos[7].rstrip()

        info_notas.append({"periodo":periodo,
                           "codigo":codigo,
                           "crn":crn,
                           "subperiodo":subperiodo,
                           "login":login,
                           "nota":nota,
                           "semestre":semestre,
                           "promedio":promedio})
    f.close()
    return info_notas

def load_encuestas():
    ruta = "../docs/cca/"
    files_names = listdir(ruta)[1:]
    cursos = []
    for file in files_names:

        f = open(ruta+file)
        crn = '"'+ file.split("_")[0].split(".")[0]+'"'#se quito el csv y se asume que se agrupan los crn por clase
        codigo = encontrar_curso_crn(crn)
        carga_promedio = 0
        satisfaccion = 0
        lines = f.readlines()[5:]#comienzan los datos
        for line in lines:
            datos = line.split(";")
            e4 =""
            e8 =""
            ht1 = datos[11].split('"')[1]# se tenia que quitar el '""'
            ht2 = datos[17].split('"')[1]
            o5 = datos[28].split('"')[1]
            c1 = datos[39].split('"')[1]
            if len(datos) >= 71:#no todoss tienen esta pregunta
                e4 = datos[71].split('"')[1]
                if len(datos[75].split('"')) > 1:#
                    e8 = datos[75].split('"')[1]
            carga_actual = datos[29].split('"')[1]
            if  0 < len(carga_actual)< 2 :#saca los que son en formatos diferentes (todos los que no seasn numeros
                carga_promedio += int(carga_actual)
            if 0 < len(ht1) <2:
                satisfaccion += int(ht1)
            if 0 < len(ht2) <2:
                satisfaccion += int(ht2)
            if 0 < len(o5) <2:
                satisfaccion += int(o5)
            if 0 < len(c1) <2:
                satisfaccion += int(c1)
            if 0 < len(e4) <2:
                satisfaccion += int(e4)
            if 0 < len(e8) <2:
                satisfaccion += int(e8)
        cursos.append({"codigo":codigo,
                       "crn":crn,
                       "carga":round(carga_promedio/len(lines),2),
                       "satisfaccion":satisfaccion})
        f.close()

    return cursos
def retiros_por_codigo(codigo):
    encontrado=-1
    for curso in cursos:
        if curso["codigo"]==codigo:
            encontrado = curso["retiros"]
            break
    return encontrado
def retiros(dic):
    return dic["retiros"]
def olap1(info):#satisfaccion y notas
    plt.figure()
    plt.title("Analisis Olap ")
    plt.xlabel("satisfaccion")
    plt.ylabel("retiros")
    for curso in info:
        retiros = retiros_por_codigo(curso["codigo"])
        plt.barh(retiros,curso["satisfaccion"])
        plt.text(curso["satisfaccion"],retiros,curso["codigo"])
    plt.show()
def olap2(info):
    plt.figure()
    plt.title("Analisis Olap")
    plt.xlabel("carga")
    plt.ylabel("retiros")
    for curso in info:
        retiros = retiros_por_codigo(curso["codigo"])
        plt.barh(retiros, curso["carga"])
        plt.text(curso["carga"], retiros, curso["codigo"])
    plt.show()

cursos = load_cursos()
info_olap = load_encuestas()
olap1(info_olap)
olap2(info_olap)