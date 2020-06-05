
import ETL2
import matplotlib.pyplot as plt

def preguntas():
    plt.figure()
    plt.title("Preguntas Respondidas 2017 y 2018")

    plt.bar(1,t1,label="2017")
    plt.bar(2, t2, label="2018")
    plt.legend()
    plt.show()
def cursos():
    plt.figure()
    plt.title("Cursos Encuestados 2017 y 2018")

    plt.bar(1,len(cursos2017),label="2017")
    plt.bar(2, len(cursos2018), label="2018")
    plt.legend()
    plt.show()

cursos2017, cursos2018, t1,t2 = ETL2.load_encuestas()
preguntas()
cursos()

