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


    f = open("docs/anon/iyr2018.csv")
    lines = f.readlines()
    info = []
    lines = lines[1:]
    for line in lines:
        datos = line.split(";")

        periodo = datos[0]
        codigo = datos[1]
        crn = datos[2]

        # 1) se quita el "" y se ponen como enteros
        retiros = int(datos[3].split('"')[1])
        inscritos = int(datos[4].rstrip().split('"')[1])

        info.append({"periodo":periodo,
                             "codigo":codigo,
                             "crn":crn,
                             "retiros":retiros,
                             "inscritos":inscritos})

    #print("la información para cursos con retiros e insritos para esta entrega es", len(lines))

    f.close()
    return info
def load_encuestas():
    #2017
    ruta = "docs/cca2017/"
    files_names = listdir(ruta)[1:]
    cursos2017 = []
    en2017 =0
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
        cursos2017.append({"codigo":codigo,
                       "crn":crn,
                       "carga":round(carga_promedio/len(lines),2),
                       "satisfaccion":round(satisfaccion/len(lines),2)})
        en2017+=len(lines)
        f.close()

    #2018
    ruta = "docs/anon/cca2018/"
    files_names = listdir(ruta)[1:]
    cursos2018 = []
    en2018 = 0
    for file in files_names:

        f = open(ruta + file)
        crn = '"' + file.split("_")[0].split(".")[
            0] + '"'  # se quito el csv y se asume que se agrupan los crn por clase
        codigo = encontrar_curso_crn(crn)
        carga_promedio = 0
        satisfaccion = 0
        lines = f.readlines()[5:]  # comienzan los datos
        for line in lines:
            datos = line.split(";")
            e4 = ""
            e8 = ""
            ht1 = datos[11].split('"')[1]  # se tenia que quitar el '""'
            ht2 = datos[17].split('"')[1]
            o5 = datos[28].split('"')[1]
            c1 = datos[39].split('"')[1]
            if len(datos) >= 72:  # no todos tienen esta pregunta
                if len(datos[71].split('"')) > 1:
                    e4 = datos[71].split('"')[1]
                    if len(datos) >= 76:
                        if len(datos[75].split('"')) > 1:  #
                            e8 = datos[75].split('"')[1]
            carga_actual = datos[29].split('"')[1]
            if 0 < len(carga_actual) < 2:  # saca los que son en formatos diferentes (todos los que no seasn numeros
                carga_promedio += int(carga_actual)
            if 0 < len(ht1) < 2:
                satisfaccion += int(ht1)
            if 0 < len(ht2) < 2:
                satisfaccion += int(ht2)
            if 0 < len(o5) < 2:
                satisfaccion += int(o5)
            if 0 < len(c1) < 2:
                satisfaccion += int(c1)
            if 0 < len(e4) < 2:
                satisfaccion += int(e4)
            if 0 < len(e8) < 2:
                satisfaccion += int(e8)
        cursos2018.append({"codigo": codigo,
                       "crn": crn,
                       "carga": round(carga_promedio / len(lines), 2),
                       "satisfaccion": round(satisfaccion / len(lines), 2)})
        en2018 += len(lines)
        f.close()
    #print("encuestas",en2017+en2018)

    return cursos2017,cursos2018,en2017,en2018
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
def olap1(info1,info2):#satisfaccion y notas
    plt.figure()
    plt.title("Cursos: Retiros vs. Satisfacción 2018")
    plt.xlabel("satisfaccion")
    plt.ylabel("retiros")
    plt.axis((0,15,0,30))
    print(info1)
    for curso in info2:
        retiros = retiros_por_codigo(curso["codigo"])
        if retiros == -1:
            continue
        plt.bar(retiros,curso["satisfaccion"],label=curso["codigo"])
    plt.show()
def olap2(info1,info2):
    plt.figure()
    plt.title("Cursos: Retiros vs. Carga Académica 2018")
    plt.xlabel("carga")
    plt.ylabel("retiros")
    plt.axis((0, 15, 0, 5))
    for curso in info2:
        retiros = retiros_por_codigo(curso["codigo"])
        if retiros == -1:
            continue
        plt.bar(retiros, curso["carga"],label=curso["codigo"])
        #plt.text(curso["carga"], retiros, )
    #plt.legend(loc="best")
    plt.show()
def olap3(info1,info2):
    plt.figure()
    plt.title("Cursos: Satisfacción vs. Carga Académica")
    #plt.title("Cursos: Retiros vs. Nota")
    plt.xlabel("satisfaccion")
    plt.ylabel("carga")
    plt.axis((0,30,0,5))
    for curso in info1:
        plt.plot(curso["satisfaccion"],curso["carga"],"or")
    for curso in info2:
        plt.plot(curso["satisfaccion"], curso["carga"], "ob")
        #plt.text(curso["carga"], retiros, )
    #plt.legend(loc="best")
    plt.show()
def olap4(info1,info2):
    plt.figure()
    plt.title("Cursos: Inscritos vs. Satisfacción 2018")
    plt.xlabel("satisfaccion")
    plt.ylabel("inscritos")
    plt.axis((0,90,0,30))
    for curso in info1:
        inscritos = inscritos_por_codigo(curso["codigo"])
        if inscritos == -1:
            continue
        plt.plot(inscritos,curso["satisfaccion"],"ob",label=curso["codigo"])
    for curso in info2:
        inscritos = inscritos_por_codigo(curso["codigo"])
        if inscritos == -1:
            continue
        plt.plot(inscritos,curso["satisfaccion"],"or",label=curso["codigo"])
    plt.show()
