# Prometeo CLI challenge 002
!['Prometeo logo'](https://cdn.prometeoapi.com/static/img/primary%402x.png)
### [**Link to the challenge**](https://joinignitecommunity.com/desafio-scraping/)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)  

## **Instalación**

### **Virtualenv**

Clonar el repo y ejecutar los siguientes comandos: 
```
python -m venv env
source env/bin/activate
python -m pip install -r requirements.txt
```

## **Descripción**

### Introducción

Se decidió obtener información de los alquileres dentro de Capital federal. Argentina.

Las páginas scrapeadas fueron las siguientes:

 1. MercadoLibre Ar
 2. Argenprop
 3. Properati

Se considerá un Item scrapeado exitoso si cumple con las siguientes condiciones:

 - Tiene imágenes (Nadie quiere alquiler un apartamento sin verlo)
 - Describe la ubicación del apartamento.
 - Posee los metros cuadrados del apartamento
 - Describe los ambientes y/o dormitorios.
 - Tiene precio  (Obviamente, jeje) y no está en dólares.

### Item

En base a lo anterior, tenemos que la estructura final de un Item será: 

- Precio
- Localización (región o barrio) 
-  Dirección exacta
- Metros cuadrados
- Expensas (si tiene)
- Imágenes
- Url
- Información adicional (baños, años, etc)

### Objetivo 

Con el scraper se busca responder las siguientes preguntas:

 - ¿Cuáles son las zonas con alquileres más baratos en relación al metro cuadrado?
 - Relación de metro cuadrado por ambiente.
 - Distribución del costo del alquiler más expensas.
 - Zonas con más alquileres disponibles. 

### Resultados

|Página| Items obtenidos |  Items descartados| Efectividad (%)
|--|--|--|--|
| `argenprop.com` | 1750 | 895 | 66.16%
| `inmuebles.mercadolibre.com.ar` |1077|939|53.42% 
| `properati.com.ar` |973|2216| 30.51%

**Nota:** La mayoría de los items descartados se debe a que los precios estaban en dólares. 
**Nota2 :** Los resultados de MercadoLibre se deben tomar cierto margen de error (dependiendo de las configuraciones del scraper), ya que la página bloquea cuando hay muchas solicitudes al mismo tiempo.

### Gráficos

Hola equipo de Prometeo, soy yo otra vez, como pueden ver, me gustan mucho los gráficos. ¿Qué cosas no?

####  Apartamentos por Barrios

Como se puede ver, hay más oferta de apartamentos (en pesos) en Palermo, Belgrano, Caballito y Flores.

Estas zonas generalmente son asociadas a la clase media / alta y están cerca de múltiples puntos importantes en la ciudad.

**Nota:** Gran parte de los datos pertenecientes a "Otros" hacen referencia a zonas relacionadas a Palermo como *Botánico* o *Hollywood*

#### Frecuencia de precios de alquileres.

Vamos con un gráfico más interesante.  Acá se calculó el precio del alquiler + expensas y organizó en un histograma con rangos de 10.000 ARS

Acá podemos ver que el rango más común está entre los 40.000 ARS  y los 90.000 ARS. Un equivalente más o menos a 200$ y 450$.

El precio más común es de 50.000 ARS ( equivalente a 250$).  

En los casos extremos podemos ver que un alquiler puede salir entre el más barato en 10.000 ARS y 310.000 ARS, osea 50$ a 1550$.,

Si nos vamos a la versión completa, el máximo aumenta hasta 4800$.

**Nota:** Esta versión está normalizada, si prefiere ver la versión completa, puede revisar los archivos. 


#### Superficie en relación a los ambientes. 

Parece una tontería. Obviamente mientras más ambientes, más espacio. ¿Verdad?

Pues si observamos la línea del promedio y los valores mínimos, sí, coincide. Pero sin duda es curioso ver los valores máximos. 

Sobre todo si notamos la gran caída en relación a 1 ambiente y 2 ambientes en la línea del valor máximo.
 
 También podemos observar algo similar en la línea de valores mínimos en relación a 6 y 7 ambientes.
 
 Y por último observamos que no hay un cambio tan significativo en promedio entre 1 y 2 ambientes.
 
 La moraleja acá es, revisar tanto los ambientes como la cantidad de m2 a la hora de comparar apartamentos. 

#### Distribución de M2 en los Barrios.

Uno de mis gráficos favoritos. 

Observamos que en zonas como Coghlan, San Telmo y Centro tienen más m2 en promedio en relación al resto de barrios.

Se podría decir que es por su relación con respecto a los valores máximos, pero no pasa lo mismo con los picos más altos en Paternal,Boedo, Charita o Caballito.

También es curioso ver la diferencia tan grande entre los máximos y el promedio. 

* **Chiste argentino:** Parece que Boca no es tan grande como decían, eh?* Sin embargo, es uno de los más homogéneos, en conjunto a Liniers. *

#### Relación de superficie / precio

Ahora sí, mi gráfico favorito. 

Se dividió el precio entre m2, para calcular el valor de 1 m2 en cada barrio. A fin de responder la primera pregunta de los objetivos.

Es un gráfico un poco complejo pero a fines prácticos se interpreta de la siguiente forma.

Mientras más grande el rectángulo, más datos se tienen dentro de ese rango. Las velas o lineas indican valores atípicos o extremos. 

De modo que para lo que nos interesa, tenemos que observar que hay un patrón entre 1100 y 1500 ARS por m2, lo cual coincide si tenemos en cuenta los gráficos anteriores.

Dicho de otra forma. Mientras más arriba la caja, más caro será ese alquiler por metro cuadrado. Mientras más pequeña la caja, los datos serán más homogéneos y no habrá mucha variación entre los precios. 

Si observamos la mitad de la caja de, Palermo, por ejemplo. Podemos ver que el precio por m2 (en la mediana) es de aproximadamente 1600 ARS.  Si tenemos en cuenta que Palermo tenía un promedio de 50 m2 ( ver gráficos anteriores).

Podemos calcular que un alquiler en Palermo estaría, normalmente, en 80.000 ARS, osea 400$


### Uso

> Mucho bla bla bla, muestra qué tengo que hacer.

Vale, vamos al grano.

```
cd reto_scraping
scrapy list | xargs -I {} -t scrapy crawl {} -O ./data/{}.json
```


**Nota** : Puede tardar un rato. Para fines de la demostración decidí quitar una configuración extra en el spider de Mercadolibre (como se mencionó antes). De modo que si le interesa conocer datos más específicos, recomiendo "descomentar" la configuración en este spider. 

Una vez terminado ejecuta el siguiente comando: 

```
python -m main
```
Esto debería crear unos gráficos, en base a los json obtenidos anteriormente. 



## Flask APP

Acá iría la explicación de la presentación y filtrado de datos en una web app con flask.

...

....

![meme](https://pbs.twimg.com/media/Dxh-29XWsAAllD4.jpg)

[Contexto del meme]( https://www.youtube.com/watch?v=knQ1agY_lWs)

