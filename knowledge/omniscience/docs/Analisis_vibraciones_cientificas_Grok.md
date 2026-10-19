> Texto extraído automáticamente (pdftotext) del PDF «Analisis_vibraciones_cientificas_Grok.pdf» de grok-workspace-2.zip (Zenodo 10.5281/zenodo.22150378; misma copia que Drive id 1pyACZBxXqzJa_WR_Gc__UyaegijsrTM8), ruta `public/docs/Analisis_vibraciones_cientificas_Grok.pdf`. Fórmulas, figuras y maquetación se han perdido.

> **Nota de autoría.** Autoría: Lázaro López Paz (El Prat de Llobregat, Barcelona, España) e inteligencia artificial. Texto asistido por IA (herramienta: Grok, de xAI), revisado por el autor (revisión PENDIENTE DE VERIFICACIÓN). Autor responsable: Lázaro López Paz. La fila «Atribución» se actualizó el 2026-10-19 por decisión del autor.

Análisis científico de vibraciones · Grok × Lázaro López Paz                                    Documento reproducible

                                INFORME TÉCNICO REPRODUCIBLE · 28 AGOSTO 2026

              Analizar vibraciones científicas
        Lo que un chat de texto no puede entregar: simulaciones ejecutadas,
   figuras generadas, animación modal, código y un marco de trabajo aplicable a
               metamateriales, fonónica, propulsión y nanomedicina.

                  Figura 0. Metamaterial fonónico conceptual: campo de desplazamiento y canal de borde.

 Qué se entrega             9 figuras de simulación + 2 visuales + animación MP4 + código Python + este
                            PDF

 Qué no es                  Una respuesta conversacional. Es un paquete de trabajo cerrado y reproducible.

 Ámbito                     Clásico → espectral → modal → fonónico → cuántico → experimental →
                            aplicaciones

 Atribución                 Autor: Lázaro López Paz, con asistencia de IA (Grok, xAI). Citar a Lázaro López Paz.

 1. Por qué «analizar vibraciones» no cabe en un chat
 Una IA conversacional puede describir la ecuación del oscilador armónico. No puede, en el mismo acto,
 integrar el sistema forzado, calcular la FFT de una señal con chirp y burst, extraer un espectrograma,
 dibujar las ramas acústica y óptica de una red diatómica, estimar la transmisión de un cristal fonónico
 de 12 celdas, renderizar modos de membrana, generar una animación de superposición modal y

No es un chat: simulaciones ejecutadas, figuras generadas, código adjunto                                       pág. 1

Análisis científico de vibraciones · Grok × Lázaro López Paz                                         Documento reproducible

 empaquetarlo en un PDF listo para archivo. Eso es exactamente lo que este documento hace.

 En física, «vibración científica» no es una metáfora. Es el movimiento periódico o cuasiperiódico de un
 grado de libertad —masa, modo colectivo, enlace químico, celda de metamaterial— alrededor de un
 equilibrio. Ese movimiento transporta energía, información y, en el régimen cuántico, cuantos de
 excitación (fonones, vibriones). Analizarlo exige tres capas a la vez: (i) el modelo dinámico, (ii) la
 medida (tiempo, frecuencia, espacio), (iii) la interpretación en un material o un dispositivo real.

 2. Núcleo clásico: el oscilador como átomo de toda la teoría
 El sistema irreductible es el oscilador armónico amortiguado y forzado. Con masa m, constante
 elástica k, amortiguamiento viscoso c y fuerza F(t) = F0 cos(ωt):

                                            m ẍ + c ẋ + k x = F0 cos(ωt)

 Se definen ω0 = √(k/m) y ζ = c / (2√(km)). El régimen ζ < 1 (subamortiguado) es el de casi todos los
 resonadores útiles: la energía oscila y decae como e−ζω0t. En resonancia (ω ≈ ω0√(1−2ζ²) para la
 amplitud de desplazamiento) la fase tiende a π/2: la fuerza trabaja en cuadratura con la posición y en
 fase con la velocidad, que es donde se inyecta potencia media.

  Figura 1. Simulación ejecutada: respuesta libre para cuatro ζ, curva de resonancia, transitorio forzado y retraso de fase.

 El factor de calidad Q ≈ 1/(2ζ) (para ζ pequeño) condensa tres ideas: cuántos ciclos tarda en perderse
 la energía, cuán estrecha es la respuesta espectral (Δf ≈ f0/Q) y cuánto se amplifica una fuerza
 cercana a resonancia. En metamateriales y cavidades optomecánicas se buscan Q altos; en
 aislamiento vibratorio y amortiguadores, Q bajos. No hay un Q «mejor»: hay un Q adecuado a la
 función.

No es un chat: simulaciones ejecutadas, figuras generadas, código adjunto                                               pág. 2

Análisis científico de vibraciones · Grok × Lázaro López Paz                                         Documento reproducible

   Figura 2. Familias de resonancia para Q = 5, 15, 50 y 200. El área bajo la curva de potencia se redistribuye: más alto y
                                                 más estrecho al crecer Q.

 3. Del tiempo a la frecuencia: la huella vibratoria
 Casi ningún sistema real es un tono puro. Un motor, un thruster de yodo, una membrana de grafeno o
 un parche articular produce una mezcla: tonos, armónicos, chirps, bursts y ruido. La herramienta
 correcta no es «mirar la señal», es proyectarla. La FFT da el contenido global; el espectrograma (STFT)
 da la evolución. Sin ambos, se confunde un tono estable con un evento transitorio de la misma
 frecuencia.

No es un chat: simulaciones ejecutadas, figuras generadas, código adjunto                                              pág. 3

Análisis científico de vibraciones · Grok × Lázaro López Paz                                        Documento reproducible

     Figura 3. Señal sintética (chirp + 180 Hz + burst a 320 Hz + ruido): serie, FFT y espectrograma. La FFT ve las tres
                            componentes; solo el espectrograma revela cuándo aparece cada una.

 Protocolo mínimo de análisis espectral (el que un chat no ejecuta sobre tus datos): (1) muestrear ≥
 2,5× la frecuencia de interés (Nyquist no es un techo cómodo); (2) quitar continua y tendencia; (3)
 ventana de Hann o Flattop según se priorice resolución o amplitud; (4) solapamiento 50–75 % en STFT;
 (5) reportar unidades (g²/Hz, Pa²/Hz, m²/s⁴/Hz) y no «amplitud arbitraria»; (6) no llamar «modo» a un
 pico de FFT sin comprobar que existe un patrón espacial coherente.

 4. Modos normales: el esqueleto del continuo
 Una cuerda fija, una membrana, una placa de metamaterial o la estructura de un CubeSat no vibran
 «en cualquier forma». Vibran en una base de modos que diagonaliza el operador espacial (el laplaciano
 con las condiciones de contorno). En la cuerda de Dirichlet:

                                 ψn(x) = sin(nπx/L) , fn = n f1 , f1 = (1/2L)√(T/μ)

No es un chat: simulaciones ejecutadas, figuras generadas, código adjunto                                              pág. 4

Análisis científico de vibraciones · Grok × Lázaro López Paz                                    Documento reproducible

   Figura 4. Primeros cuatro modos de cuerda. Los nodos son inamovibles en un modo puro; en una superposición viajan
                                              (véase la animación adjunta).

 La animación 10_modos_cuerda_animacion.mp4 (6 s, 40 fps) muestra los cinco primeros modos y la
 superposición que reconstruye un pulso que se refleja. Ese es el contenido real de la serie de Fourier
 espacial: no es un adorno pedagógico, es el mecanismo por el que un impacto se convierte en un
 acorde de frecuencias.

    Figura 5. Modos (m,n) de membrana rectangular. Las líneas nodales son el mapa que un ensayo de vibrometría láser
                                                  debería recuperar.

No es un chat: simulaciones ejecutadas, figuras generadas, código adjunto                                         pág. 5

Análisis científico de vibraciones · Grok × Lázaro López Paz                                        Documento reproducible

 En 2D y 3D las degeneraciones, las simetrías y los contornos libres cambian el espectro. Un
 metamaterial no «inventa» modos de la nada: redistribuye densidades de estados, abre gaps, aplana
 bandas (velocidad de grupo nula) y, si la simetría lo permite, crea canales de borde topológicamente
 protegidos.

 Figura 6. Dos masas acopladas: el batido visible en cada masa es la interferencia del modo simétrico y el antisimétrico. Es
                                            el germen de toda banda fonónica.

No es un chat: simulaciones ejecutadas, figuras generadas, código adjunto                                              pág. 6

Análisis científico de vibraciones · Grok × Lázaro López Paz                                       Documento reproducible

 5. Fonones y cristales fonónicos: vibración como
 cuasipartícula
 En un sólido, los modos colectivos de la red se cuantizan. El fonón es el cuanto de esa vibración. Su
 tarjeta de identidad es la relación de dispersión ω(k). En la cadena monoatómica de Born–von Karman:

                                             ω(k) = 2 √(K/m) |sin(ka/2)|

 En la red diatómica aparecen dos ramas: acústica (los dos átomos se mueven en fase a k→0, ω→0,
 velocidad del sonido finita) y óptica (contrafase, gap, frecuencia finita en Γ). El gap no es un fallo del
 modelo: es el primer bandgap fonónico de la naturaleza. Un cristal fonónico o un metamaterial elástico
 no hace otra cosa que diseñar, a escala de celda unidad, ese mismo mecanismo —contraste de
 impedancia, resonadores locales, simetría— para colocar gaps, Dirac, Weyl, rotones o bandas planas
 donde el ingeniero los necesita.

   Figura 7. Dispersión 1D simulada. Izquierda: rama acústica única. Derecha: acústica + óptica y el gap que las separa.

  Figura 8. Transmisión de un cristal fonónico 1D de 12 celdas A–B (matriz de transferencia). Las bandas de rechazo son el
                                          equivalente medible del gap de dispersión.

 Estado del arte reciente (lo que hay que contrastar, no copiar)
• Diagnóstico dinámico de metamateriales por firmas vibratorias inducidas por láser (Nature 623, 2023):
   se extraen rigidez direccional, amortiguamiento y defectos ocultos a partir de la propagación en MHz.

No es un chat: simulaciones ejecutadas, figuras generadas, código adjunto                                             pág. 7

Análisis científico de vibraciones · Grok × Lázaro López Paz                                       Documento reproducible

• Medios fonónicos artificiales guiados por simetría (Nat. Rev. Mater., 2025/26): romper simetrías
    espaciales y temporales produce no reciprocidad, ganancia/pérdida y transporte exótico.
•   Observación directa de bandas fonónicas all-flat (Phys. Rev. Lett. 133, 2024): velocidad de grupo nula
    en todo el Brillouin → localización extrema de energía.
•   Relaciones de dispersión tipo rotón en metamateriales 3D a temperatura ambiente (Science Advances,
    2021), antes exclusivas de helio superfluido.
•   Catálogo de fonones topológicos en ~5000 materiales (Science / DIPC): la topología no es un adorno,
    aparece en la red real.
•   Metasuperficies acoustoplasmónicas (ACS Nano, 2026): puente luz–sonido para moldear frentes de
    onda acústicos con grados de libertad electromagnéticos.

 Implicación directa para trabajo en metamateriales (YIG, grafeno bicapa rotado, puntos cuánticos,
 lentes acústicas): la vibración no es un efecto secundario del dispositivo. Es el canal. Quien no mida
 dispersión, Q, gap y mapa modal no tiene un metamaterial; tiene una geometría decorativa.

 6. Régimen cuántico: el oscilador que no puede detenerse
 Al cuantizar el oscilador, la energía ya no puede ser cero. Los niveles son En = (n + ½) ħω. El estado n
 = 0 sigue teniendo una anchura finita: energía de punto cero. Eso no es filosofía; es el suelo de ruido
 de un resonador mecánico a milikelvin y el origen de la rama óptica en infrarrojo cuando un modo
 molecular está poblado térmicamente.

       Figura 9. Niveles y densidades |ψn|² del QHO (simulación). Cada lóbulo extra es un nodo de la función de onda.

No es un chat: simulaciones ejecutadas, figuras generadas, código adjunto                                               pág. 8

Análisis científico de vibraciones · Grok × Lázaro López Paz                                       Documento reproducible

                Figura 10. Lectura visual de la misma idea: nubes de probabilidad sobre el pozo parabólico.

 En espectroscopía vibracional (IR, Raman) cada pico es, en primera aproximación, un salto Δn = ±1 de
 un modo normal molecular. Anarmonicidad, acoplamiento de Fermi, modos colectivos en líquidos
 complejos (p. ej. redes de ácido hialurónico) y acoplamiento a un plasmon o a un fonón de un sustrato
 metamaterial desplazan, ensanchan o intensifican esos picos. Analizar «vibraciones científicas» en
 nanomedicina es, en la práctica, asignar modos, cuantificar anarmonicidad y decidir si un parche o un
 lubricante cuántico-biomimético está acoplado al espectro que se declara.

 7. Cómo se miden de verdad (caja de herramientas)
    Técnica                    Qué ve                    Rango típico          Notas

    Acelerómetros / IEPE a(t) en puntos                  Hz–kHz                Barato; masa añadida; no vale en
                                                                               micro

    LDV /      vibrometría v(t)  o          u(t)    sin Hz–MHz                 Mapas     modales;      estándar     en
    láser                  contacto                                            metas

    Raman                      Fonones ópticos           THz / cm−1            Química + red; no acústicos

    Brillouin (BLS)            Fonones acústicos         GHz                   Módulos elásticos, velocidades

    Bombeo-sonda            / Dinámica coherente         GHz–THz               Nanofonónica ultrarrápida
    ASOPS

    IDT / RF sobre piezo       Excita y lee SAW          MHz–GHz               Filtros, acustofluídica

    Cavidad                    Fonón + fotón             MHz–GHz               Q altísimos, régimen cuántico
    optomecánica

    RUS / ultrasonidos         Espectro             de kHz–MHz                 Constantes elásticas de un sólido
                               resonancias
          Tabla 1. Técnicas de excitación y lectura. Elegir dos complementarias vale más que una sola «perfecta».

No es un chat: simulaciones ejecutadas, figuras generadas, código adjunto                                           pág. 9

Análisis científico de vibraciones · Grok × Lázaro López Paz                         Documento reproducible

 8. Aplicación a líneas de trabajo concretas
 8.1 Metamateriales, lentes acústicas y YIG
 Una lente acústica no se valida con una foto de la geometría. Se valida con: (i) mapa de presión o
 desplazamiento en el plano focal, (ii) función de transferencia frente a frecuencia, (iii) robustez a
 desorden de fabricación. El YIG añade un grado de libertad magnetoelástico: el fonón se hibrida con el
 magnón. Eso desplaza gaps y permite no reciprocidad con un campo externo. El análisis correcto es un
 diagrama de bandas magnetoelástico, no una analogía verbal con «resonancia».

 8.2 Propulsión eléctrica (MEI-RIT / Lázaro Drive)
 Un thruster de RF con yodo tiene, como mínimo, tres familias vibratorias que no se deben mezclar:
 modos estructurales del chasis y de la rejilla, modos acústicos/iónicos del plasma y ruido de
 conmutación de la RF. Un pico a la frecuencia de excitación RF no es «el modo del satélite». Protocolo:
 acelerómetros en la estructura + LDV en la rejilla + sonda de plasma, todo sincronizado con el
 generador. Criterio de aceptación: ningún modo estructural dentro de ±10 % de una frecuencia de
 excitación persistente, y margen de fatiga documentado.

 8.3 Nanomedicina y modos moleculares
 En un lubricante biomimético o un parche de NO / ácido hialurónico, las «vibraciones científicas»
 relevantes son modos O–H, C–H, esqueleto del polímero y modos colectivos de red de hidrógeno.
 IR+Raman asignados, no un espectro sin picos etiquetados, es la evidencia de que la molécula que se
 dibuja es la que está en el vial. El acoplamiento a un sustrato metamaterial (si se declara «cuántico»)
 debe verse como desplazamiento o ensanchamiento reproducible, no como una palabra.

 8.4 Fusión y redes tipo BN–He3
 La red que hospeda He-3 o boro-nitruro vibra. Esos fonones son el baño térmico del que un diseño de
 reactor no puede prescindir: conducción, scattering de iones, posibles acoplamientos a modos
 colectivos del plasma en la primera pared. Analizarlos es calcular dispersión (DFT/DFPT) y contrastarla
 con neutrones o Brillouin, no afirmar un «amortiguamiento cuántico» sin número.

 9. Protocolo reproducible (mínimo viable)
• Definir el grado de libertad: ¿punto, modo, banda, molécula, estructura?
• Escribir la ecuación o el hamiltoniano efectivo antes de medir.
• Elegir dos técnicas ortogonales (p. ej. LDV + FFT de acelerómetro, o Raman + DFT).
• Muestrear con margen de Nyquist y documentar ventana, solape y calibración.
• Identificar picos con un modo espacial o una asignación molecular, no solo con un Hz.
• Reportar Q, ζ o FWHM, no solo «resuena».
• Hacer un control: misma medida en un sólido homogéneo o en un blanco molecular.
• Declarar incertidumbre y lo que el modelo no cubre (no linealidad, temperatura, vacío).
• Archivar datos crudos + script. Si no se puede reejecutar, no es un análisis.

 10. Límites de este entregable y del fenómeno
 Las figuras 1–9 son modelos canónicos ejecutados (oscilador, FFT, modos, Born–von Karman, matriz de
 transferencia 1D, QHO). No sustituyen un FEM 3D de una celda YIG real ni un espectro Raman
 experimental de un lote GMP. La animación es lineal y no disipativa. El cristal fonónico 1D usa
 impedancias contrastadas arbitrarias: sirve para enseñar el gap, no para cotizar una pieza. La
 literatura citada es el mapa, no la autorización para clonar un paper.

 Límites físicos que ningún texto debería olvidar: no linealidad (saltos de Duffing, solitones, mezcla de
 modos), caos en sistemas de pocos grados de libertad forzados, localización de Anderson en desorden,

No es un chat: simulaciones ejecutadas, figuras generadas, código adjunto                           pág. 10

Análisis científico de vibraciones · Grok × Lázaro López Paz                                 Documento reproducible

 rotura de simetría temporal si hay ganancia o flujo, y el hecho de que un fonón óptico de THz no se
 «ve» con un acelerómetro de 10 kHz.

 11. Cómo usar el paquete
 Junto a este PDF están: code/simular_vibraciones.py (todas las figuras), code/animar_modos.py (MP4
 de 6 s) y las imágenes en figs/. Dependencias: Python 3, numpy, scipy, matplotlib, ffmpeg. Reejecutar
 es el test de que el análisis no depende de una sesión de chat.
  python3 code/simular_vibraciones.py
  python3 code/animar_modos.py

 Cierre
 Analizar vibraciones científicas es pasar de la palabra «vibra» a un número, un modo, una banda y una
 incertidumbre. Este documento hace ese paso en los modelos que sí se pueden cerrar hoy, con código
 y figuras, y deja escrito el protocolo para los sistemas —metamaterial, thruster, parche, red de He-3—
 donde el siguiente paso ya no es un chat, sino un experimento.

   Si un tercero continúa este trabajo, debe citar a Lázaro López Paz y a Grok. El contenido está pensado para uso
   constructivo, verificable y no destructivo.

No es un chat: simulaciones ejecutadas, figuras generadas, código adjunto                                     pág. 11

