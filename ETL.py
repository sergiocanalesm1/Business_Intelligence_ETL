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

    f = open("docs/iyr.csv")
    lines = f.readlines()
    info_retiros = []
    lines = lines[1:]
    for line in lines:
        datos = line.split(";")

        periodo = datos[0]
        codigo = datos[1]
        crn = datos[2]
        retiros = datos[3].split('"')[1]
        inscritos = datos[4].rstrip().split('"')[1]

        info_retiros.append({"periodo":periodo,
                             "codigo":codigo,
                             "crn":crn,
                             "retiros":int(retiros),
                             "inscritos":int(inscritos)})

    f.close()
    return info_retiros

def load_notas():
    sub = {}
    f = open("docs/nota.csv")
    lines = f.readlines()
    info_notas = []
    lines = lines[1:]
    p=0
    c=0
    for line in lines:
        datos = line.split(";")
        periodo = datos[0]
        subperiodo = datos[1].split('"')[1].replace("B","")
        codigo = datos[2]
        crn = datos[3]
        login = datos[4]
        nota = datos[5]
        if nota != '""':
            nota = float(datos[5].split('"')[1].replace(",","."))
            p += nota
        else:
            nota = "-"
            c+=1
        semestre = datos[6]
        promedio = datos[7].rstrip()
        info_notas.append({"periodo":periodo,
                           "codigo":codigo,
                           "crn":crn,
                           "subperiodo":int(subperiodo),
                           "login":login,
                           "nota":nota,
                           "semestre":semestre,
                           "promedio":promedio})
        if subperiodo not in sub.keys() and nota != '-':
            sub[subperiodo] = nota
        else:
            if nota != '-':
                sub[subperiodo] += nota
        p = p / (len(lines)-c)
    f.close()
    return info_notas

def load_encuestas():
    ruta = "docs/cca/"
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
                       "satisfaccion":round(satisfaccion/len(lines),2)})
        f.close()

    return cursos
def retiros_por_codigo(codigo):
    encontrado=-1
    for curso in cursos:
        if curso["codigo"]==codigo:
            encontrado = curso["retiros"]
            break
    return encontrado
def inscritos_por_codigo(codigo):
    encontrado=-1
    for curso in cursos:
        if curso["codigo"]==codigo:
            encontrado = curso["inscritos"]
            break
    return encontrado

def retiros(dic):
    return dic["retiros"]
def olap1(info):#satisfaccion y notas
    plt.figure()
    plt.title("Cursos: Retiros vs. Satisfacción")
    plt.xlabel("satisfaccion")
    plt.ylabel("retiros")
    for curso in info:
        retiros = retiros_por_codigo(curso["codigo"])
        if retiros == -1:
            continue
        plt.barh(retiros,curso["satisfaccion"],label=curso["codigo"])
        #plt.text(curso["satisfaccion"],retiros,curso["codigo"])
    #plt.legend(loc="best")
    plt.show()
def olap2(info):
    plt.figure()
    plt.title("Cursos: Retiros vs. Carga Académica")
    plt.xlabel("carga")
    plt.ylabel("retiros")
    for curso in info:
        retiros = retiros_por_codigo(curso["codigo"])
        if retiros == -1:
            continue
        plt.barh(retiros, curso["carga"],label=curso["codigo"])
        #plt.text(curso["carga"], retiros, )
    #plt.legend(loc="best")
    plt.show()
def olap3(info):
    plt.figure()
    plt.title("Cursos: Satisfacción vs. Carga Académica")
    #plt.title("Cursos: Retiros vs. Nota")
    plt.xlabel("satisfaccion")
    plt.ylabel("carga")
    plt.axis((0,30,0,5))
    for curso in info:
        plt.plot(curso["satisfaccion"],curso["carga"],"or")
        #plt.text(curso["carga"], retiros, )
    #plt.legend(loc="best")
    plt.show()
def olap4(info):
    plt.figure()
    plt.title("Cursos: Inscritos vs. Satisfacción")
    plt.xlabel("satisfaccion")
    plt.ylabel("inscritos")
    plt.axis((0,90,0,30))
    for curso in info:
        inscritos = inscritos_por_codigo(curso["codigo"])
        if inscritos == -1:
            continue
        #plt.bar(inscritos,curso["satisfaccion"],label=curso["codigo"])
        plt.plot(inscritos,curso["satisfaccion"],"ob",label=curso["codigo"])
        #plt.text(inscritos+1,curso["satisfaccion"]+1,curso["codigo"],fontsize=4)
    #plt.legend(loc="best")
    plt.show()


cursos = load_cursos()
info_olap = load_encuestas()
notas = load_notas()


olap1(info_olap)
olap2(info_olap)
olap3(info_olap)
olap4(info_olap)


