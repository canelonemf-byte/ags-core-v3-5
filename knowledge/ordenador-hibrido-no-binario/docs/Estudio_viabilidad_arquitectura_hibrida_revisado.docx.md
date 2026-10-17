> Texto extraído automáticamente del PDF original «Estudio_viabilidad_arquitectura_hibrida_revisado.docx.pdf». Fórmulas, figuras y maquetación se han perdido; el original está en Drive: https://drive.google.com/file/d/1_HFmRCW88Bx4nu2N_FQ2VNR0Ntoj0CEX/view?usp=drivesdk



Lóp ez Paz  ·  Monografía de viabilidad  ·  arq uitectura híbrida  ·  2 0 2 6  

ESTUDIO CONCEPTUAL DE VIABILIDAD  ·  MONOGRAFÍA COMPLETA 

Arq uitectura  híbrida  multinivel de ultra -ba jo 
consumo 

Límites físicos, estado del arte, diseño de sistema, 
evaluación rep roducible y p lan de investigación de p rincip io a fin 

Lá za ro Lóp ez Pa z 

Estudio indep endiente  ·  Lleida, Catalunya 

8  de sep tiembre de 2 0 2 6  

Versión comp leta  revisa da   ·  no exp erimenta l  ·  sin coa utoría  de modelos de IA 

Aviso  de  integrida d.  Este  documento  es  una   monogra fía   de  via b ilida d.  Recorre  la   p regunta   desde  los  límites 
termodiná micos  ha sta   un  p la n  de  I+D  con  hitos  fa lsa b les.  No  describ e  un  p rototip o  fa b rica do p or el a utor, no 
rep orta   curva s  I–V  ni netlists p rop ios, y no a trib uye a  su firma nte la  invención de memristores, dica lcogenuros, 
modula dores  fotónicos,  a utóma ta s  de  p untos  cuá nticos,  comp uta ción  con  ADN  ni  a lgoritmos  cuá nticos.  Esa s 
línea s  p ertenecen  a   comunida des  identifica da s  en  la s  referencia s.  La s  cifra s  son  (a )  consta ntes  física s,  (b ) 
a ritmética  p eda gógica  con hip ótesis escrita s en la  misma  p á gina , o (c) órdenes de ma gnitud toma dos de a rtículos 
cita dos.  Un  ma nuscrito  p revio  mezcla b a   esa s  ca tegoría s  con  « resulta dos  de simula ción»  no rep roducib les. Esa  
p rá ctica  se ha  elimina do. La  semeja nza  con p royectos a ctivos se decla ra : este texto es una  síntesis crítica , no el 
cua derno de la b ora torio de un grup o a jeno. 

Resumen ejecutivo 

La p regunta q ue abre el estudio es antigua y reap arece cada vez q ue un disp ositivo muestra más de 
dos  estados  estables:  ¿ p uede  construirse  un ordenador cuya rep resentación de la información no se 
limite  al  código  binario  y  q ue  sea  estrictamente  sup erior  al  CMOS  binario  actual  en  velocidad, 
consumo  energético  y  temp eratura  de  op eración a la vez?  Desp ués de recorrer la termodinámica, la 
teoría de la información, el estado real de los disp ositivos y las restricciones de software, la resp uesta 
es no en el sentido global y sí en un sentido local y esp ecializado. 

El p rincip io de Landauer fija una cota mínima p ara borrar información de forma irreversible: k_B T 
ln  2   p or  bit,  unos  2 ,8 7 × 1 0 ⁻²¹ J a 3 0 0  K (ap roximadamente 1 8  meV). Si en lugar de un bit se borra un 
dígito de base b, la cota es k_B T ln b, p ero ese dígito transp orta log₂ b bits. La energía mínima p or bit 
de información no cambia al p asar a ternario, cuaternario o a una base mayor. « Dejar de ser binario»  
no es un atajo termodinámico. La única vía concep tual p ara bajar de esa cota p or op eración útil es no 
borrar:  comp utación  lógicamente  reversible,  ejecutada  lo  bastante  desp acio  como p ara recup erar la 
energía almacenada en la cap acidad del nodo. Incluso entonces, todo p roceso a tiemp o finito p roduce 
entrop ía extra. 

Eso  no  cierra  el  p roblema  de  ingeniería.  Los  p rocesadores  de  2 0 2 6   siguen  disip ando,  p or 
conmutación  y  sobre  todo  p or  movimiento  de  datos,  muchos  órdenes  de  magnitud  p or  encima  de 
Landauer. El límite p ráctico de la lógica de muchos niveles a temp eratura ambiente no es esa cota, sino 

Documento concep tual — sin datos exp erimentales p rop ios  ·  p ágina 1  

Lóp ez Paz  ·  Monografía de viabilidad  ·  arq uitectura híbrida  ·  2 0 2 6  

el ruido térmico kT/C, el desajuste de umbrales, la variabilidad ciclo a ciclo de las memorias resistivas, 
el coste de los conversors y el hecho de q ue comp iladores, redes, sistemas op erativos y memorias de 
masa seguirán siendo binarios durante décadas. 

La  evidencia  p ublicada  ap unta  a  una  arq uitectura  heterogénea,  no  a  un  p rocesador  de  un  solo 
radix.  Un  núcleo  CMOS  binario  de  p rop ósito  general  p ara  el  código  irregular y el sistema op erativo; 
bloq ues  de  memoria  resistiva  multinivel  (RRAM  de  HfOₓ  u  óxido  eq uivalente)  p ara  p roducto 
matriz-vector y p esos no volátiles; fotónica de silicio o híbrida allí donde el cable metálico es el cuello 
de botella; y un comp ilador o p lanificador q ue decida q ué kernel corre en q ué dominio físico. La lógica 
de tres o cuatro niveles, si se usa, debe vivir en islas locales con buen margen eléctrico, no como ISA de 
todo el sistema. Esa combinación p uede reducir julios p or op eración útil en cargas regulares —álgebra 
lineal  densa,  inferencia,  filtrado  digital—  sin  p retender  ganar  a  la  vez  densidad  de  integración, 
p rogramabilidad general y madurez de foundry. 

Este  texto  no  asigna  « p robabilidades  de  éxito»   del  7 0   %  o  del  1 0   %.  Esas  cifras,  sin  un  modelo 
bayesiano  exp lícito  ni  datos  de  p roceso,  son  retórica.  En  su  lugar  se  sep aran  tres  tesis  de  distinta 
solidez. Tesis A: sup erar al CMOS binario en todas las métricas de sistema con una sola tecnología no 
binaria es, con el conocimiento actual, imp lausible como objetivo de ingeniería a q uince años. Tesis B: 
obtener  ventaja  energética  local  en  aceleradores  híbridos  es  p lausible  y  ya  hay  demostraciones 
p arciales en PIM, NPU y fotónica. Tesis C: convertir esas demostraciones en un módulo comp arable a 
un  SoC  comercial  exige  una  década  o  más  de  integración,  fiabilidad,  herramientas  y  software,  con 
coste de unos p ocos millones de euros en consorcio académico o de cientos de millones si se acomete 
como p rograma industrial. 

Recomendación  op erativa:  acotar  el  p rograma  a  un  acelerador  de  ultra-bajo  consumo  p ara  un 
conjunto cerrado de kernels, con baseline p úblico, sin narrativa de « ordenador del futuro q ue sustituye 
al binario» . Esa narrativa no resiste la literatura ni la física, y no hace falta p ara justificar el trabajo. 

Índice de contenidos 

1 .  Introducción  —  2 .  Funda mentos  físicos  y  límites  —  3 .  Fa milia s  tecnológica s  —  4 .  Arq uitectura s 
p rop uesta s  —  5 .  Cómo  eva lua r  —  6 .  Síntesis  de  evidencia   p ub lica da   —  7 .  Discusión  —  8 .  Pla n  de 
investiga ción y desa rrollo — 9 . Conclusiones — 1 0 . Limita ciones — 1 1 . Autoría  y ética  — 1 2 . Glosa rio 
— 1 3 . Referencia s — Anexo A. Cá lculos — Anexo B. Corresp ondencia  con el La TeX origina l — Anexo C. 
Lista  de comp rob a ción. 

1 . Introducción 

1 .1  Motiva ción 

El ordenador digital contemp oráneo es binario p or razones históricas y de ingeniería, no p orq ue la 
naturaleza solo conozca dos estados. Shannon mostró q ue cualq uier fuente discreta p uede codificarse 
en  bits  sin  p érdida  de  información;  el  transistor  de  efecto  de  camp o  ofrece  de  forma  natural  dos 
regiones  de  op eración  robustas  (corte  y  conducción);  las  memorias,  los buses y los comp iladores se 
construyeron  sobre  esa  convención.  El  resultado  no  es  solo  un  transistor:  es  un  ecosistema 
—conjuntos  de  instrucciones,  sistemas  op erativos,  redes,  herramientas  de  síntesis,  foundries, 

Documento concep tual — sin datos exp erimentales p rop ios  ·  p ágina 2  

Lóp ez Paz  ·  Monografía de viabilidad  ·  arq uitectura híbrida  ·  2 0 2 6  

estándares  de  memoria—  cuyo  coste  hundido  sup era  con  creces  el  de  cualq uier  laboratorio  de 
disp ositivos. 

Esa  hegemonía  no  imp lica  q ue dos sea el único radix físicamente p osible. Un condensador p uede 
almacenar  más  de  dos  voltajes  distinguibles;  un  filamento  de  óxido  p uede  p resentar  varias 
conductancias; un resonador fotónico p uede sintonizarse en varios p untos de fase o de amp litud; una 
célula electroq uímica o una molécula p uede ocup ar más de dos configuraciones. A finales de los años 
cincuenta,  en  la  Universidad  Estatal  de  Moscú,  se  construyó  el  Setun,  un  comp utador  ternario 
eq uilibrado.  Desde  entonces,  la  lógica  multi-valuada  (MVL)  ha  p roducido  una  literatura  continua de 
p uertas, sumadores, LUT y, más tarde, circuitos en CNTFET y en disp ositivos emergentes. La p regunta 
no  es  si  se  p uede  rep resentar  un  número  en  base  3   o  4 .  La  p regunta  es  si  conviene  hacerlo  en un 
sistema q ue tiene q ue convivir con el mundo binario y con el ruido de 3 0 0  K. 

Tres p resiones hacen q ue la p regunta no sea ociosa. Primera: el final relativo del escalado clásico de 
Dennard. Bajar V_DD ya no entrega la misma reducción de p otencia dinámica sin p agar en variabilidad 
y  en  fugas.  Segunda:  el  coste  energético  de  la  inteligencia  artificial  a  escala  de  centro  de  datos, 
dominado  p or  el  movimiento  de  p esos  y  activaciones  más  q ue  p or  la  ALU.  Tercera: una cosecha de 
disp ositivos —RRAM, PCM, TMD, fotónica integrada, lógicas ferroeléctricas— q ue de forma natural son 
analógicos  o  multinivel.  Ignorarlos sería tan dogmático como p roclamar q ue van a jubilar al CMOS el 
año q ue viene. 

1 .2  Pregunta  de investiga ción 

Pregunta  p rincip al.  ¿ Existe,  o  p uede  existir  en  un  horizonte de diez a q uince años, un sistema de 
cómp uto  cuya  rep resentación  de  la  información  no  se  limite  a  dos  niveles  lógicos  y  q ue  sea 
estrictamente  sup erior a un p rocesador CMOS binario de nudo comp arable en tres ejes simultáneos: 
latencia  o  frecuencia  efectiva,  energía  p or  op eración  útil  y  temp eratura  de  op eración  (o,  de  forma 
eq uivalente, densidad de p otencia disip ada)?  

Preguntas  derivadas.  Si  la  resp uesta  global  es  negativa,  ¿ en  q ué  cap as  del  sistema  (disp ositivo, 
circuito,  microarq uitectura,  interconexión,  software)  un  radix  distinto  de  2   o  una  rep resentación 
continua  ap orta  ventaja  neta?   ¿ Qué  métrica  hay  q ue  op timizar  —julios  p or  MAC,  julios  p or  bit  de 
resultado,  op eraciones  p or  vatio  a  iso-latencia—  p ara no autoengañarse con un núcleo más frío q ue 
hace menos trabajo útil?  ¿ Qué p artes del p roblema son de física y cuáles son de ecosistema?  

1 .3  Objetivos 

1 .  Enunciar los límites físicos q ue cualq uier p rop uesta no binaria debe resp etar, con las fórmulas y las 
hip ótesis a la vista. 
2 .  Inventariar las familias tecnológicas relevantes distinguiendo lo demostrado en laboratorio, lo q ue 
está en foundry y lo q ue es p rosp ecto. 
3 .  Prop oner arq uitecturas de sistema en las q ue cada rep resentación viva donde la física lo justifica, 
no donde q ueda bien en un diagrama. 
4 .  Definir un p rotocolo de evaluación rep roducible, en sustitución de tablas de simulación no 
p ublicables. 
5 .  Redactar un p lan de I+ D p or fases con hitos falsables, riesgos, bandas de p resup uesto y criterios de 
abandono. 
6 .  Dejar exp lícita la frontera entre la contribución de este texto (síntesis crítica y p lan) y la de los 
grup os q ue fabrican disp ositivos. 

Documento concep tual — sin datos exp erimentales p rop ios  ·  p ágina 3  

Lóp ez Paz  ·  Monografía de viabilidad  ·  arq uitectura híbrida  ·  2 0 2 6  

1 .4  Alca nce y no a lca nce 

Dentro del alcance. Termodinámica de la información; ruido y márgenes; lógica multi-valuada como 
circuito; memorias resistivas multinivel; fotónica integrada como tejido de datos; FET 2 D y TFET como 
candidatos a bajo V_DD; comp utación reversible y adiabática como p rograma a largo p lazo; software e 
ISA como restricción de diseño; un p lan de trabajo de 8  a 1 4  años. 

Fuera  del  alcance.  Fabricación  de  disp ositivos  p or  el  autor.  Camp añas  de  medida.  Un  ISA 
cuaternario de p rop ósito general. Un sistema op erativo nuevo. Un ordenador de ADN. Un p rocesador 
cuántico  como  sustituto  del  clásico. Una solicitud formal de financiación. La q uímica detallada de un 
stack de óxido concreto, q ue p ertenece a q uien lo dep osita. 

1 .5  Método 

El método es el de una revisión estructurada con diseño de sistema. Primero se fijan las cotas q ue 
no  se  p ueden  negociar.  Desp ués  se  examina  cada  familia  tecnológica  con  tres  p reguntas:  q ué  hace 
mejor q ue el CMOS binario, q ué hace p eor, y en q ué bloq ue de un SoC tendría sentido. A continuación 
se  comp onen  tres  arq uitecturas candidatas a nivel de bloq ues —sin netlists inventados— y se define 
cómo debería medirse una ventaja p ara q ue un revisor indep endiente p udiera rep roducirla. Por último 
se escribe un p lan de I+ D cuya virtud p rincip al es p oder fracasar en una fase concreta sin arrastrar el 
resto del relato. 

No  se  ejecuta  un  flujo  EDA  industrial.  No  se  p resenta  un  cuaderno  Jup yter  como  p rueba  de  un 
material.  Donde  el  manuscrito  original  incluía  VQE,  algoritmos  genéticos,  PINN  y  Grover  como si ya 
hubieran p roducido un p rocesador, este texto exp lica p ara q ué servirían esas herramientas si se usaran 
bien y p or q ué no constituyen un resultado. 

1 .6  Rela ción con el tra ba jo p revio (decla ra ción de no a p rop ia ción) 

La idea de q ue la base óp tima de numeración es cercana a e ≈ 2 ,7 1 8 , y p or tanto el 3 , ap arece en 
análisis  clásicos  de  coste  de  rep resentación  (Hayes  y la literatura de op timal radix). La crítica de q ue 
ese  argumento  no  se  traduce  en  circuitos  mejores  la  ha  desarrollado  con detalle Daniel Etiemble al 
comp arar p uertas, sumadores y multip licadores ternarios y cuaternarios con sus eq uivalentes binarios: 
el  recuento  de  transistores  suele  crecer  más  q ue  el  factor  log₂  b.  La  lógica multinivel en CMOS, I²L, 
CNTFET  y  disp ositivos  emergentes  está revisada p or Andreev et al. (Advanced Materials, 2 0 2 2 ) y p or 
décadas de trabajo de K. C. Smith, Current y otros. 

El p rincip io de Landauer (1 9 6 1 ) y su generalización a lógica N-aria (Bormashenko, 2 0 2 0 ; Kycia, 2 0 2 0 ) 
establecen q ue la cota p or bit no mejora al cambiar de base. La comp utación reversible y adiabática es 
el  p rograma  de  Bennett, Fredkin, Toffoli, Likharev, Lent, Frank y otros. Los memristores y el cómp uto 
en memoria se asocian a Chua, Strukov, Williams, Ielmini, Xia y a una literatura industrial de RRAM de 
HfOₓ.  La  fotónica  integrada  con  memoria  de  cambio  de  fase  o  memristores  óp ticos  tiene 
demostraciones  recientes  (memresonadores  III–V  sobre  silicio,  PCM  en  guías).  Los  FET de MoS₂ y el 
p ap el de las vacantes de azufre son un camp o masivo y anterior a este texto. El Setun y el argumento 
ternario soviético p ertenecen a Brusentsov y a la historia de la comp utación. 

La arq uitectura « híbrida CMOS–memristor–fotónica con lógica de p ocos niveles»  no es un invento 
aislado: es la intersección, declarada como tal, de tres comunidades. Lo q ue este estudio ap orta es el 

Documento concep tual — sin datos exp erimentales p rop ios  ·  p ágina 4  

Lóp ez Paz  ·  Monografía de viabilidad  ·  arq uitectura híbrida  ·  2 0 2 6  

filtro  de  viabilidad  conjunta  —ruido,  software,  termodinámica,  hoja  de  ruta—  y  la  corrección  de 
sobrecitas y cifras no sustentadas de un borrador anterior. 

1 .7  Estructura  del resto del documento 

El  cap ítulo  2   desarrolla  los  límites.  El  3   inventaría  tecnologías.  El  4   p rop one  tres  arq uitecturas  y 
describe el flujo de un GEMM. El 5  sustituye las tablas inventadas p or un p rotocolo. El 6  resume lo q ue 
sí se p uede afirmar citando a otros. El 7  discute tesis, comp romisos, software y riesgos. El 8  detalla el 
p lan de I+ D. El 9  concluye. Los anexos recogen cálculos, la trazabilidad resp ecto al LaTeX de p artida y 
una lista de comp robación. 

2 . Funda mentos físicos y límites 

2 .1  El p rincip io de La nda uer 

En  1 9 6 1   Rolf  Landauer  observó  q ue  el  borrado  irreversible  de  información  tiene  un  coste 
termodinámico.  En  un  baño  a  temp eratura  T,  cuando  un  bit  está  en  un  estado  eq uip robable  e 
indep endiente del resto del sistema, resetearlo a un valor conocido disip a al menos 

E_L  ≥  k_B T ln 2  

con k_B =  1 ,3 8 0 6 4 9 × 1 0 ⁻²³ J/K. A 3 0 0  K, k_B T ln 2  ≈ 2 ,8 7 × 1 0 ⁻²¹ J ≈ 1 7 ,9  meV ≈ 2 ,8 7  zJ. Esa cota no 
dice  q ue cada transistor de un iPhone disip e 1 8  meV. Dice q ue no se p uede borrar un bit irreversible 
p or  debajo  de  esa energía media si se op era en contacto con un baño a T. Los CMOS actuales están, 
p or conmutación de un nodo lógico, entre cientos y millones de k_B T según el nudo, la cap acidad y si 
se cuenta o no el movimiento de datos hasta la DRAM. 

La  cota  se  generaliza.  Si  el  p roceso  lógico  no  es  un  reset  p erfecto,  o  si  los  estados  no  son 
eq uip robables,  el  calor  mínimo  involucra  la  entrop ía  de  Shannon  de  la  información  descartada 
condicionada  a  la  salida  (Reeb  y  Wolf,  y  trabajos  p osteriores  de  termodinámica  estocástica).  Si  el 
p roceso ocurre en tiemp o finito τ, ap arece un término extra de p roducción de entrop ía q ue escala, en 
muchos modelos, como 1 /τ. Landauer es el caso cuasiestático. 

2 .2  Ca mbio de ba se: p or q ué el trit no a horra  p or bit 

Un  dígito en base b, si los b símbolos son eq uip robables, transp orta log₂ b bits. El borrado de ese 
dígito, en las mismas hip ótesis de Landauer, cuesta al menos k_B T ln b. El cociente es 

(k_B  T ln b)  / log₂  b  =   k_B T ln 2  

La cota p or bit de información es indep endiente de la base. Quien comp are « energía p or símbolo»  
entre  un  bit  y  un  trit  sin  dividir  p or  la  información  está  cometiendo  un  error  dimensional. 
Bormashenko y Kycia han escrito esta observación con detalle p ara lógica N-aria; no es un resultado de 
este estudio, es un teorema de la termodinámica de la información. 

Consecuencia de diseño: un argumento q ue emp iece p or « p asamos a base 4  y p or tanto gastamos 
menos»  está, en el mejor de los casos, hablando de otra magnitud (símbolos de interconexión, número 
de hilos, área de un bus) y, en el p eor, vendiendo un milagro q ue la física no autoriza. 

Documento concep tual — sin datos exp erimentales p rop ios  ·  p ágina 5  

Lóp ez Paz  ·  Monografía de viabilidad  ·  arq uitectura híbrida  ·  2 0 2 6  

2 .3  Comp uta ción reversible 

Si  la  función  lógica  es  biyectiva  —la  salida  determina  de  forma  única  la  entrada—  no  hay,  en 
p rincip io,  q ue  borrar.  Bennett  mostró  q ue  cualq uier  cómp uto  se  p uede  volver  reversible  a  costa de 
esp acio y de tiemp o, cop iando la salida y deshaciendo los p asos intermedios. Las p uertas de Toffoli y 
de Fredkin son el alfabeto discreto de ese p rograma. Likharev, Lent y Frank, entre otros, lo han llevado 
a circuitos y a CMOS adiabático. 

Tres p recios. Esp acio: hay q ue guardar basura q ue luego se destejerá. Tiemp o: la adiabaticidad p ide 
ramp as  largas  frente  a  la  constante  RC.  Reloj:  hace  falta  una  red  de alimentación resonante de alto 
factor  de  calidad  si  se  q uiere  recup erar  de  verdad  la  energía  de  señal.  Una  arq uitectura  multinivel 
adiabática es coherente sobre el p ap el; no hay un microp rocesador comercial q ue la imp lemente. Este 
estudio la reserva a la arq uitectura B, de p rop ósito esp ecial. 

2 .4  Conmuta ción a dia bá tica  en CMOS 

En  CMOS  convencional,  cargar  un  condensador  C  hasta  V a través de un interrup tor conectado a 
una fuente de voltaje constante disip a ~ ½ C V² en la resistencia del camino. Al descargar se disip a el 
otro medio. Toda la energía q ue salió de la fuente acaba en calor. Si la fuente no es un escalón sino una 
ramp a  de  duración  τ  ≫  RC,  la  disip ación  p or  transición  tiende,  en  el  modelo  de  ramp a lineal, a un 
término del orden de 
 E_dis  ≈  (R  C / τ)  C V²  

Si  τ  =   1 0  RC, se disip a del orden de una décima de C V² en lugar de un medio. El p recio es q ue el 
flanco duró diez constantes de tiemp o: la frecuencia útil baja o el reloj se vuelve un objeto de diseño 
tan difícil como la lógica. Sin un resonador de alto Q, « adiabático»  es solo un CMOS lento. 

2 .5  Ruido térmico, misma tch y má rgenes entre niveles 

En  un  nodo  cap acitivo  en  eq uilibrio  con  el  baño,  el  teorema  de  fluctuación-disip ación  da  una 
varianza de voltaje k_B T / C. La desviación típ ica es 

σ  =   √(k_B  T / C)  

A  T  =   3 0 0   K y C =  1  fF, σ ≈ 2 ,0 4  mV. Si se emp aq uetan b niveles en un rango V_DD, la sep aración 
nominal  es  ΔV =  V_DD / (b − 1 ). La tabla 1  no es un resultado de laboratorio. Es aritmética con esas 
dos hip ótesis. Sirve p ara ver cómo se estrecha el margen, no p ara dimensionar un chip . 

Base  b  ΔV a  V_DD =  0,50  V (mV)  ΔV / σ (C =  1  fF)  Lectura  cualit a tiva  
2   500   ≈ 246   Margen holgado a este C 
3   250   ≈ 123   Aún holgado; el coste está 
en el circuito 
4   167   ≈ 82   Viable si la variabilidad de 
umbral es baja 
8   71   ≈ 35   Empie za a compe tir con 
offset y mismatch 
16   33   ≈ 16   Frágil a 300  K sin C mayor o 
T menor 

Tabla  1.  Separación  entre niveles frente a  ruido kT/C. Hipót esis: un solo nodo, ruido térmico blanc o, sin 1/f , sin mismat ch ni 
ac oplamien to. En silicio real  el presupues to de ruido es peor . 

Tres consecuencias de diseño. Primera: aumentar C mejora σ, p ero encarece energía dinámica (~ C 
V²)  y  retardo.  Segunda:  el  criterio  de  error  no  es  solo  ΔV/σ;  hay  q ue  integrar  colas,  offset  de 

Documento concep tual — sin datos exp erimentales p rop ios  ·  p ágina 6  

Lóp ez Paz  ·  Monografía de viabilidad  ·  arq uitectura híbrida  ·  2 0 2 6  

comp aradores, deriva y envejecimiento. Una regla tosca de comunicaciones p ide varios σ entre niveles 
p ara una BER baja; el mismatch de un p ar en un nudo avanzado p uede ser de milivoltios a decenas de 
milivoltios.  Tercera:  en  memoria  resistiva  los  « niveles»   son  conductancias,  no  voltajes  de  un  único 
condensador, y el enemigo p rincip al es la variabilidad ciclo a ciclo y disp ositivo a disp ositivo. 

2 .6  Ca p a cida d de ca na l y SNR 

La cap acidad de un canal gaussiano blanco de banda B y relación señal/ruido S/N es 

C  =   B log₂  (1  +  S/N)    bit/s 

El  número  efectivo  de  niveles  de amp litud distinguibles escala, en orden de magnitud, con la raíz 
del  SNR  de  p otencia.  Eso  exp lica  p or  q ué  las  comunicaciones  usan  constelaciones densas cuando el 
SNR  es  alto,  y  binario  cuando  no  lo  es.  Trasladar  esa  intuición  al  interior  de  un  chip   es delicado: el 
« canal»  de una p uerta no es un enlace de radio. Tiene mismatch, 1 /f, acop lamiento, y un recep tor q ue 
es otro transistor, no un demodulador de laboratorio. 

2 .7  El a rgumento de la  ba se e y la  crítica  de los circuitos 

Hay un argumento clásico de rep resentación: p ara escribir un entero grande N con dígitos de coste 
unitario, el coste escala como b / ln b y se minimiza cerca de e ≈ 2 ,7 1 8 . De ahí la tentación de declarar 
el 3  « óp timo»  y el 4  « casi óp timo» . El argumento es correcto p ara ese modelo de coste. En un circuito 
CMOS el coste de un dígito no es unitario: crece con el número de umbrales, fuentes de alimentación, 
decodificadores y comp robaciones de margen. 

Daniel Etiemble y otros han comp arado inversores, NAND, sumadores y multip licadores ternarios y 
cuaternarios  con  sus  eq uivalentes  binarios  en  CNTFET  y  en  CMOS.  El  recuento  de  transistores  del 
bloq ue  multi-valuado  suele  ser  más  de  dos  veces  el  del  bloq ue  binario  q ue  transp orta  la  misma 
información.  Además,  el  cuaternario  necesita  un  V_DD  mayor  p ara  sep arar  niveles,  mientras q ue el 
binario  p uede  bajar  el  voltaje.  En  p roducto  energía-retardo,  el  binario  a  0 ,4 5   V  gana  a  menudo  al 
cuaternario a 0 ,9  V. Por eso este estudio no declara q ue « la base óp tima es 3  o 4 »  como teorema de 
disp ositivo. Declara algo más débil: 3  y 4  son los únicos radices densos con alguna op ortunidad de ser 
comp etitivos en bloq ues locales; 8  y 1 6  casi siemp re p ierden p or ruido o p or el coste del interfaz con el 
resto del sistema, q ue seguirá siendo binario. 

2 .8  Velocida d de conmuta ción y movilida d 

Una  cota  tosca  de  frecuencia  de  un inversor es f_max ≈ 1  / (2 π R_on C_gate). R_on baja cuando 
sube la movilidad y cuando el disp ositivo conduce con más corriente p or unidad de ancho. El grafeno 
se cita a menudo con 2 0 0  0 0 0  cm²/V·s. Esa cifra es el límite intrínseco imp uesto p or fonones acústicos 
en  grafeno  susp endido,  o  valores  de  laboratorio  en  condiciones  ideales.  Sobre  SiO₂,  a  3 0 0   K,  las 
movilidades típ icas de disp ositivos reales están en 5  0 0 0 –2 0  0 0 0  cm²/V·s; encap sulado en hBN p ueden 
subir  a  varias  decenas  de  miles.  Usar  2 0 0   0 0 0   como  si  fuera  el  número  de  un  interconector  de 
p roducto es un error de p rosp ecto. 

Los  TMD  (MoS₂,  WSe₂)  tienen  movilidades  más  modestas  q ue el grafeno, p ero ofrecen gap  y p or 
tanto  I_on/I_off  usable  en  lógica.  Los  TFET  p rometen  p endientes  subumbrales  p or  debajo  de  6 0  
mV/dec y, con ello, V_DD más bajos. El p recio histórico ha sido la corriente de ON insuficiente. Ninguno 
de estos materiales autoriza a escribir « 8  GHz contra 5  GHz»  sin un diseño cerrado. 

Documento concep tual — sin datos exp erimentales p rop ios  ·  p ágina 7  

Lóp ez Paz  ·  Monografía de viabilidad  ·  arq uitectura híbrida  ·  2 0 2 6  

2 .9  Temp era tura  de op era ción y densida d de p otencia  

La  temp eratura  de  un  encap sulado  no  es  un  número  q ue  se  obtenga  con  una  ODE  de  un 
comp artimento y se p ubliq ue como 5 5  °C frente a 9 0  °C. El modelo mínimo de un nudo térmico es 

C_th dT/dt  =   P_dis(t)   −   G_th (T  −  T_amb)  

C_th y G_th dep enden del encap sulado, del disip ador, del airflow o de la p laca fría, no del radix. Un 
sistema más eficiente p uede correr más fresco a igual rendimiento, o más ráp ido a igual p resup uesto 
térmico.  Lo  segundo  es  a  menudo  más  valioso  en  un  centro  de  datos.  La  métrica  correcta  no  es 
« grados  Celsius  del  núcleo» .  Es  julios  p or  op eración  útil a iso-throughp ut, o op eraciones p or vatio a 
iso-latencia, con un modelo térmico de p aq uete. 

2 .1 0  Qué se sigue de este ca p ítulo 

Landauer  no  mata  ni  salva  un  p royecto  de  lógica  multinivel  en  2 0 2 6 :  todavía  no  estamos  ahí. El 
ruido, el mismatch y el interfaz con un mundo binario sí p ueden matarlo. La reversibilidad es el único 
camino  concep tual  hacia  disip aciones  sub-Landauer  p or  op eración  útil,  y  cobra un p eaje de tiemp o, 
área y reloj. El diseño honesto elige un p unto en esa frontera y lo declara. 

3 . Fa milia s tecnológica s 

Cada familia se evalúa como p ieza de un eventual sistema híbrido. Ninguna, p or sí sola, sustituye a 
un SoC binario general. Se indica el estado y el p ap el q ue se le asigna. 

3 .1  CMOS bina rio: el ba seline q ue ha y q ue vencer 

El CMOS binario de nudo avanzado (FinFET, GAA) es la referencia. Ofrece densidad, EDA, foundries, 
comp iladores  y  un  ecosistema  de  memoria.  Su  debilidad  no  es  « ser  binario» .  Es  el  coste  de  mover 
datos  entre  SRAM,  caches  y  DRAM, la energía de las colas de una red neuronal cuando los p esos no 
caben  en  el  chip ,  y  el  suelo  de  V_DD  imp uesto  p or  el  ruido  y  las  fugas.  Madurez:  foundry.  Pap el: 
control, código irregular, sistema op erativo, y anfitrión de los aceleradores. 

3 .2  Lógica  multinivel en silicio y en CNTFET 

La  MVL  clásica  usa  transistores  de  varios  umbrales,  fuentes  múltip les  o  comp aradores  p ara 
distinguir  3   o  4   niveles  de  voltaje.  Hay  inversores,  NAND,  LUT  cuaternarios  y  sumadores p ublicados 
desde  los  años  ochenta  y,  más  tarde,  en  tecnologías  CNTFET  de  3 2   nm  de  modelo  Stanford.  Las 
ventajas declaradas son menos hilos p ara la misma información y, a veces, menos etap as en un carry. 
Las  desventajas  medidas  en  p ap ers  de  comp aración  son  más  transistores  p or  bit  eq uivalente,  más 
sensibilidad al ruido y un V_DD q ue no se p uede bajar tanto como en el binario. 

Pap el honesto: islas locales de 2  bits p or hilo si un bus concreto está saturado de metal, o bloq ues 
aritméticos de estudio. No: ISA de un Linux cuaternario. 

3 .3  Ma teria les 2 D, MoS₂ y va ca ntes de a zufre 

MoS₂  y  otros  TMD  p ermiten  canales  de  esp esor  atómico  y,  en demostraciones, p uertas lógicas a 
V_DD de unas décimas de voltio, incluso en sustratos flexibles. Las vacantes de azufre generan estados 
en  el  gap ,  dop aje  tip o  n no intencional, histéresis e inestabilidad de umbral. La literatura reciente se 

Documento concep tual — sin datos exp erimentales p rop ios  ·  p ágina 8  

Lóp ez Paz  ·  Monografía de viabilidad  ·  arq uitectura híbrida  ·  2 0 2 6  

dedica tanto a ap rovechar esos estados (conmutación resistiva, ruido p ara circuitos estocásticos, lógica 
op toelectrónica  ternaria  o  cuaternaria  en  un  solo  disp ositivo)  como  a  p asivarlos  p ara  FET  fiables 
(tioles, recocido en azufre, ingeniería de interfaz). 

Presentar « MoS₂ con vacantes»  como un material descubierto p or un algoritmo variacional de dos 
q ubits sería incorrecto: es uno de los defectos más estudiados del material. Un FET multinivel exigiría 
umbrales rep roducibles y sep aración de estados estable en oblea, no tres mesetas en una curva I–V de 
laboratorio. Pap el: candidato a canal de bajo V_DD en una fase tardía, si una foundry lo ofrece; no es la 
p ieza de la q ue dep ende el p lan entero. 

3 .4  Gra feno e interconexiones 

El  grafeno  es  un  excelente  conductor  bidimensional  y  un  mal  interrup tor  lógico  p or  ausencia  de 
gap .  Su  sitio  natural,  si  lo  tiene  en  esta  arq uitectura,  es  el  de  interconexión  o  de  electrodo 
transp arente,  no  el  de  transistor  de  un  ALU.  Las  movilidades  de  p roducto  deben  tomarse  de 
disp ositivos sobre sustrato o encap sulados, no del límite de 2 0 0  0 0 0  cm²/V·s. 

3 .5  Memristores y RRAM de HfOₓ 

Un memristor, en la acep ción de disp ositivo usada en ingeniería, es un elemento cuya conductancia 
dep ende  de  la  historia  de la tensión o de la corriente. La RRAM de HfO₂ (y stacks HfOₓ/Al₂O₃, HfAlO, 
etc.) es comp atible con el back-end de CMOS. El mecanismo habitual es la formación y rup tura de un 
filamento  de  vacantes  de  oxígeno.  Controlando la corriente de cump limiento o el voltaje de reset se 
obtienen varios estados de resistencia. Se han mostrado 4 –8  estados en arrays, y en algunos trabajos 
más,  con  el  comp romiso  clásico  entre  número  de  niveles,  ventana,  variabilidad  y  energía  de 
p rogramación. 

El  valor  sistémico  no  es  « hacer  un  ALU  cuaternario  con  memristores» .  Es  reducir  el  tráfico 
CPU–memoria: p roducto matriz-vector analógico o digital de baja p recisión, p esos no volátiles, lógica 
en  memoria.  Los  p roblemas  abiertos  son  endurance  (a  menudo  1 0 ⁴–1 0 ⁷  ciclos  según  el  stack  y  el 
algoritmo  de  escritura),  retención  a  temp eratura  de  soldadura  y  de  uso,  el selector q ue evite sneak 
p aths en un crossbar, y el coste energético y de área de los ADC/DAC. Eso ya es un p rograma industrial. 
No hace falta vestirlo de ordenador no binario universal. 

Madurez:  disp ositivos  y  macros  en  foundry  o  en  líneas  p iloto;  sistemas  comp letos  aún  de 
investigación. Pap el: corazón de la arq uitectura A. 

3 .6  Fotónica  integra da , PCM y memristores electro-óp ticos 

Mover un bit a través de un milímetro de metal es caro en energía y latencia a medida q ue crece el 
chip   o  el  módulo.  Guías  de  silicio,  p eines  de  frecuencia,  materiales  de  cambio  de  fase  (GST,  SbS)  y 
memristores electro-óp ticos p ermiten p onderar y acumular en el dominio óp tico. Hay demostraciones 
de memorias no volátiles fotónicas con energías de escritura en el rango de 0 ,1 5  p J a unos p ocos p J p or 
evento en disp ositivos de laboratorio, y estimaciones de motores in-memory fotónicos en torno a 0 ,2  
p J/MAC  bajo  hip ótesis  de  WDM  y  de tasa elevadas. Esas cifras son de los grup os q ue las midieron o 
modelaron; no se reutilizan aq uí como « resultado p rop io» . 

LiNbO₃,  sobre  todo  en  p elícula  delgada,  es  un  material  electro-óp tico  de  referencia  p ara 
moduladores. No es un p rocesador. El cuello de botella de un tile fotónico p asa a ser la conversión E/O 

Documento concep tual — sin datos exp erimentales p rop ios  ·  p ágina 9  

Lóp ez Paz  ·  Monografía de viabilidad  ·  arq uitectura híbrida  ·  2 0 2 6  

y  O/E,  el  área  de  anillos,  la  corrección  de  fase  y  la  temp eratura.  La fotónica gana cuando el lote de 
datos es grande y regular; p ierde en control irregular y en densidad frente a SRAM. 

Madurez:  PIC  comerciales p ara comunicaciones; cómp uto fotónico aún en p rototip o. Pap el: tejido 
de datos entre tiles y, si el área lo p ermite, un motor GEMM fotónico op cional. 

3 .7  Esp intrónica  

MTJ, SOT-MRAM y lógicas de dominio magnético ofrecen no volatilidad y, en algunos casos, lógica. 
El  coste  es  la corriente de escritura, el camp o local o materiales p oco estándar en foundry digital. La 
MRAM ya es memoria embebida en algunos nodos. Como ALU multinivel no ha desp lazado al CMOS. 
Pap el: memoria no volátil de ap oyo, no núcleo de cómp uto de este p lan. 

3 .8  Autóma ta s celula res de p untos cuá nticos (QCA) 

Las QCA de Lent, Tougaw y Porod rep resentan el bit p or la configuración de carga de una celda de 
p untos  cuánticos  y  p rop agan  la  información  p or  interacción  de Coulomb, casi sin corriente. Sobre el 
p ap el  se  acercan  a  disip aciones  sub-Landauer  si  el  reloj  es  lo  bastante  adiabático.  Las 
imp lementaciones  metálicas  o  semiconductoras  de  decenas  de  nanómetros  op eran  a  temp eratura 
criogénica.  La  op eración  a  3 0 0   K  exige  celdas  de  escala  molecular  (~1   nm) o QCA magnética. Tratar 
QCA  como  candidata  a  un  ordenador  de  escritorio  a  temp eratura  ambiente  sin  esa  salvedad  sería 
engañoso. Se deja como ciencia básica, no como fase 1 . 

3 .9  Puntos cuá nticos como disp ositivo de memoria  o de lógica  

Un  p unto  cuántico  p uede  alojar  un  número  discreto  de  electrones  y,  en  p rincip io,  más  de  dos 
estados. En la p ráctica, a 3 0 0  K el esp aciado energético suele ser comp arable a kT salvo q ue el p unto 
sea muy p eq ueño y muy controlado. Hay memorias y fotodetectores; no hay un datap ath de p rop ósito 
general. Pap el: fuera del camino crítico. 

3 .1 0  ADN y comp uta ción molecula r 

El  ADN  es  extraordinario  como  archivo  denso  (Church,  Goldman  y  trabajos  p osteriores)  y  como 
sustrato  de circuitos q uímicos p aralelos y lentos. Las velocidades p or molécula están muy p or debajo 
del  GHz  electrónico.  La  ventaja,  si  existe,  es  el  p aralelismo  masivo  y  una  energía  p or  op eración 
p otencialmente baja a costa de tiemp o y de microfluídica. No es un sustituto de la ALU de un CPU, ni 
un camino p ara « bajar la temp eratura del p ortátil» . Se excluye del p lan de integración de los cap ítulos 
4  y 8 . 

3 .1 1  Cop rocesa dores cuá nticos 

Un cop rocesador cuántico no es un ordenador no binario clásico. Op era en un esp acio de Hilbert y 
exige, en las p lataformas actuales, criogenia o condiciones esp eciales, corrección de errores y un cuello 
de  botella  clásico  de  control.  Puede  ser  relevante  p ara  subrutinas  muy  concretas  cuando  esas 
máq uinas  maduren. Incluirlo en el mismo diagrama de bloq ues q ue un FET cuaternario de 0 ,3  V solo 
añade confusión. Queda como interfaz futura op cional (arq uitectura C), no como p ilar de la eficiencia 
del chip  clásico. 
 Documento concep tual — sin datos exp erimentales p rop ios  ·  p ágina 1 0  

Lóp ez Paz  ·  Monografía de viabilidad  ·  arq uitectura híbrida  ·  2 0 2 6  

3 .1 2  Inteligencia  a rtificia l p a ra  el co-diseño 

La IA no es un material. Es útil en tres sitios honestos: búsq ueda de p arámetros de disp ositivo con 
DFT/NEGF o modelos surrogate (no con un VQE de dos q ubits p resentado como hallazgo); síntesis de 
circuitos  bajo  restricciones;  y  p lanificación  en  tiemp o  de  ejecución  de un SoC heterogéneo. Usar un 
algoritmo  de  Grover  « p ara  buscar  contraejemp los»   de  una  arq uitectura  de  chip   no  constituye 
verificación formal. La verificación de hardware se hace con model checking, eq uivalencia y simulación 
de gate-level. La búsq ueda cuántica no ap orta aq uí un atajo p ublicable. 

Familia   Madur ez  Papel  en el sistema  híbrido  Qué no se le pide  
CMOS binario  Foundry  CPU, control, ISA, OS  Que desapar ezca 
MVL 3–4   Paper s / algunos chip s  Islas locales, buses cortos  Un Linux cuaternario 
TMD / MoS₂  Lab +  líneas pilot o  FET de bajo V_DD a medio 
plaz o  Que «descubr amos»  sus 
vacantes 
RRAM HfOₓ  Macros y arrays  MAC in-memory, pesos  NV  ALU exacta de 64  bits 
Fotónica +  PCM  PIC +  pr ototipos   Movimiento de datos, 
GEMM denso  Control irregular 

MRAM / espín   Memoria embebida  NV de apo yo  Sustituir el datapa th 
QCA  Ciencia básica  Fuera del plan  8–14  años  CPU a 300  K en metal 
ADN  Archivo / lab químic o  Excluido  Bajar T del port átil 
Cuántico  NISQ / early FT  Interfaz futura opcional   Ahorro energético del SoC 
IA de diseño  Software  Búsqueda  y orques tación  Coautoría ni 
«descubrimien to»  

Tabla  2.  Papel  honesto de cada  familia  en un sistema  híbrido  de ultra-bajo  consumo. 

4 . Arq uitectura s p rop uesta s 

4 .1  Princip io de diseño 

Cada  rep resentación de la información debe vivir donde su física es una ventaja y morir donde es 
un  estorbo.  El  voltaje  multinivel  es  frágil  en  un  bus  largo  y  ruidoso;  la  conductancia  multinivel  es 
natural  en  un  crossbar  q ue  ya  es  analógico; la amp litud o la fase óp ticas son naturales en un enlace 
q ue ya es fotónico; el bit es natural en el sistema op erativo. El diseño no busca un radix único. Busca 
un contrato entre dominios, con traductores exp lícitos y con un p resup uesto de error en cada frontera. 

4 .2  Arq uitectura  A — Acelera dor heterogéneo CMOS +  RRAM +  fotónica  de da tos 

Esta es la candidata central. Se describe p or bloq ues. 

Bloq ue  anfitrión.  Un  CPU  CMOS  binario  de  nudo  comercial  (o  un  cluster  de  núcleos)  ejecuta  el 
sistema op erativo, el runtime, las excep ciones y el código irregular. Habla un ISA binario. No ve q uits. 

Bloq ue  de  cómp uto  en  memoria.  Uno  o  varios  tiles  1 T1 R  o  1 S1 R  de  RRAM  de  HfOₓ.  Cada cruce 
almacena  un  p eso  como conductancia en N niveles (N =  4  u 8  como objetivo de ingeniería, no como 
dogma).  Las  activaciones  se  inyectan  como  voltajes  o  como  p ulsos.  La  ley  de  Ohm  y  las  leyes  de 
Kirchhoff realizan un p roducto matriz-vector. Los convertidores y los acumuladores digitales cierran el 
MAC. La p recisión nativa es baja o media (2 –8  bits eq uivalentes). La exactitud de una red se recup era 
con cuantización consciente del hardware, no con un ALU de 6 4  bits resistivo. 

Bloq ue de datos locales. SRAM binaria como scratchp ad y como cola de activaciones. El multinivel 
no se usa p ara el p rogram counter. 

Documento concep tual — sin datos exp erimentales p rop ios  ·  p ágina 1 1  

Lóp ez Paz  ·  Monografía de viabilidad  ·  arq uitectura híbrida  ·  2 0 2 6  

Bloq ue de tejido. Entre tiles distantes, un enlace fotónico de silicio (o un interp oser con PIC) cuando 
el  volumen  de  un  lote  justifica  la  conversión  E/O.  Entre  vecinos,  cobre.  El criterio no es estético: es 
julios p or bit-milímetro y ocup ación de área. 

Bloq ue  de  control.  Un  p rogramador  de  p esos,  un  motor  de  calibración  (la  RRAM  deriva),  y  un 
runtime q ue decide si un kernel baja al array, al CPU o —si existe— al motor fotónico. 

Software.  Comp ilador  sobre  un  IR  tip o  MLIR  o  TVM.  El  modelo  entra  en  FP1 6   o  INT8   y  sale 
map eado a conductancias. El p rogramador de ap licaciones no escribe lógica cuaternaria. 

Por  q ué  es la candidata central: cada p ieza tiene literatura y, en el caso CMOS y en p arte RRAM y 
SiPh, vías de foundry. El riesgo es de integración y de software, no de violar Landauer. 

4 .3  Arq uitectura  B — Bloq ues a dia bá ticos o reversibles de p rop ósito esp ecia l 

Un  datap ath  reversible  p ara  kernels  de  longitud  fija  (filtros  FIR,  transforms,  algunos  cifrados, 
p ip elines  de  longitud  conocida)  p uede  reducir  energía  dinámica si se acep ta un reloj más lento y un 
área  mayor.  La  codificación p uede ser binaria; el multinivel es op cional y p robablemente secundario. 
Hace falta un reloj resonante de alto Q y un diseño q ue no tire la información en cada flanco. Esta línea 
es  de  alto  riesgo  científico  y  de  bajo  encaje  comercial  a  corto  p lazo,  p ero  es  la  única  q ue  ataca  de 
frente  la  cota  de  borrado.  Se  mantiene  como  p aq uete  de  investigación  p aralelo,  no  como  camino 
crítico del acelerador A. 

4 .4  Arq uitectura  C — Interfa z futura  a  un cop rocesa dor cuá ntico 

Un  p uerto  clásico  —cola  de  trabajos, memoria de comp artición, convertidores de control— hacia 
una QPU externa. No se diseña la QPU. No se cuenta su criogenia en el p resup uesto térmico del SoC. 
Se reserva la p osibilidad de offload de subrutinas (muestreo, algunos kernels de q uímica) cuando esa 
máq uina exista y cuando el coste de ida y vuelta no se coma la ventaja. Incluir la C en el mismo titular 
q ue la A sería p ublicidad. 

4 .5  Lo q ue no se p rop one 

●  Un CPU cuaternario de p rop ósito general q ue ejecute Linux con un ISA incomp atible. 
●  Un « ordenador de ADN»  ni un SoC de QCA metálica a 3 0 0  K. 
●  Sustituir el binario en memoria p rincip al, discos, redes y comp iladores. 
●  Una cifra única de « cinco veces mejor»  como meta contractual. 
●  Coautoría de un modelo de lenguaje como si hubiera dirigido un laboratorio. 

4 .6  Flujo de una  op era ción típ ica  (ejemp lo GEMM) 

7 .  El runtime recibe una multip licación de matrices a p recisión 8  bits (o la p recisión q ue el modelo 
tolere). 
8 .  Los p esos, si no están ya en el array, se p rograman en las conductancias con el algoritmo de 
escritura del stack (p ulsos con verify). Ese coste se amortiza si los p esos se reutilizan. 
9 .  Las activaciones llegan desde SRAM o desde el enlace fotónico, convertidas al dominio q ue el tile 
esp era. 
1 0 . El array realiza el MAC. Los ADC o los acumuladores digitales entregan un tensor binario. 
1 1 . El CPU no ve q uits: recibe ese tensor, ap lica la no linealidad o la normalización q ue no merezca la 
p ena hacer en analógico, y encadena la siguiente cap a. 

Documento concep tual — sin datos exp erimentales p rop ios  ·  p ágina 1 2  

Lóp ez Paz  ·  Monografía de viabilidad  ·  arq uitectura híbrida  ·  2 0 2 6  

1 2 . Un monitor de error estima la deriva del array y disp ara una recalibración si la exactitud del 
modelo cae p or debajo del umbral p actado. 

5 . Cómo eva lua r, en luga r de inventa r ta bla s 

5 .1  Qué se ha  retira do y p or q ué 

El  manuscrito  original  incluía  tres  tablas  p resentadas  como  resultado  de  simulación:  energías  y 
retardos  de  una  AND  cuaternaria  « híbrida»   (7   fJ,  6   p s)  frente  a  una  AND  CMOS  (1 0   fJ,  5   p s);  un 
sumador de 1  bit frente a un sumador cuaternario; y un cuadro global con 0 ,2  p J frente a 1  p J, 8  GHz 
frente  a  5   GHz,  5 5   °C  frente  a  9 0   °C, 7 0  M p uertas/mm² frente a 1 0 0  M, y « cinco veces mejor» . Sin 
netlist, modelo de transistor, rincón de p roceso, p atrón de actividad y encap sulado, esas cifras no son 
rep roducibles. No se reutilizan aq uí ni como orden de magnitud p rop io. 

También  se  han  retirado  el  VQE  como  descubrimiento de materiales, el algoritmo genético como 
diseño  ya  concluido  de  p uertas,  Grover  como  verificación  y  la  ODE  térmica  como  p redicción  de 
temp eratura  de  p roducto.  Conservar  la  narrativa  y  q uitar  solo  las  cifras  habría  sido  cosmético.  Se 
cambia el estatuto ep istémico: este documento op ina con argumentos y cita medidas ajenas; no finge 
un banco de p ruebas. 

5 .2  Protocolo q ue sí sería  p ublica ble 

1 3 . Fijar un baseline CMOS binario en un nudo declarado (p or ejemp lo un PDK académico de 2 8  nm o 
1 6  nm, o el q ue el consorcio p ueda p agar), con el mismo p resup uesto de error q ue el sistema 
p rop uesto. 
1 4 . Definir kernels de referencia y una métrica p rimaria: p icojulios p or MAC eq uivalente o p or bit de 
resultado, a una latencia máxima fijada, a una temp eratura de encap sulado fijada. 
1 5 . Sep arar en la cuenta energía de cómp uto, de memoria, de conversión A/D o E/O, de reloj y de 
control. La ventaja de un array memristivo suele estar en no mover p esos, no en la ALU. 
1 6 . Incluir variabilidad (Monte Carlo o medidas de array), retención, endurance y tasa de error. Una 
ventaja de 5 ×  q ue exige recalibración constante no es una ventaja de sistema. 
1 7 . Publicar modelos, netlists o, como mínimo, los p arámetros comp actos y los scrip ts. Sin eso el 
estudio p ermanece en el terreno de la op inión informada —q ue es, hoy, el terreno de este texto—. 

5 .3  Kernels mínimos 

●  GEMM 1 0 2 4 × 1 0 2 4  a 8  bits y a 4  bits, con y sin los p esos residentes en el array. 
●  Una cap a convolucional rep resentativa (p or ejemp lo 3 × 3 , 6 4  canales) como p uente hacia redes 
reales. 
●  Un sumador de 6 4  bits eq uivalentes (3 2  q uits si alguien insiste en la comp aración de radix) p ara no 
esconder el coste de la aritmética exacta. 
●  Un filtro FIR de orden fijo, como rep resentante de DSP regular. 
●  Un kernel irregular (recorrido de grafo o decodificación) p ara demostrar q ue el CPU binario sigue 
siendo necesario. 
 Documento concep tual — sin datos exp erimentales p rop ios  ·  p ágina 1 3  

Lóp ez Paz  ·  Monografía de viabilidad  ·  arq uitectura híbrida  ·  2 0 2 6  

5 .4  Métrica s 

Primaria:  energía  p or  op eración  útil  eq uivalente  (p J/MAC  o  p J/bit  de  resultado),  a  iso-calidad 
numérica  y  a  iso-latencia  de  lote.  Secundarias:  área  del  tile,  densidad  de  p otencia del encap sulado, 
BER o degradación de exactitud de la red, ciclos de endurance consumidos p or inferencia o p or ép oca 
de entrenamiento, latencia de p rogramación de p esos, y esfuerzo de software medido en semanas de 
comp ilador hasta el p rimer kernel correcto. La temp eratura se rep orta como consecuencia del modelo 
de p aq uete, no como titular. 

5 .5  Sobre a lgoritmos genéticos, PINN y VQE bien usa dos 

Nada imp ide usar un algoritmo genético o un buscador p or refuerzo p ara exp lorar top ologías de un 
bloq ue, si la función de ap titud sale de un simulador de circuito calibrado y si se p ublica la semilla, la 
p oblación  y  el  frente  de  Pareto.  Nada  imp ide  una PINN p ara un p roblema térmico de p aq uete, si se 
valida  contra  un  FEM.  Nada  imp ide,  a  medio  p lazo,  métodos  cuánticos  o  híbridos  de  q uímica  p ara 
defectos, si se comp aran con DFT y con medida. Lo q ue se p rohíbe aq uí es el atajo retórico: un listado 
de  veinte  líneas  de  Python  como  p rueba  de  q ue  el  material,  la  p uerta  o  la  arq uitectura  ya  están 
resueltos. 

6 . Síntesis de evidencia  p ublica da  

6 .1  Qué se p uede a firma r sin un la bora torio p rop io 

Sin  medidas  p rop ias  solo  se  p ueden  afirmar  regularidades  q ue  la  literatura  ya  ha  establecido  y 
órdenes  de  magnitud  q ue  varios  grup os  han  rep ortado  de forma indep endiente. Lo q ue sigue no es 
una meta-análisis estadístico; es una lectura de ingeniería. 

6 .2  Ma teria les y disp ositivos 

Las vacantes de azufre en MoS₂ generan estados en el gap  y afectan umbral, histéresis y fiabilidad; 
tanto  su  ap rovechamiento  como  su  p asivación  están  documentados.  La  RRAM  de  HfOₓ  admite 
múltip les  estados  de  resistencia  con  algoritmos  de  p rogramación  con  verify;  la  variabilidad  crece  al 
ap retar el número de niveles. El grafeno de interconexión no debe p resup uestarse a 2 0 0  0 0 0  cm²/V·s. 
Los TFET siguen limitados p or I_on en la mayoría de demostraciones. 

6 .3  Circuitos multi-va lua dos frente a  bina rios 

En  aritmética  general  p ublicada  (sumadores  y  multip licadores  ternarios  y  cuaternarios  frente  a 
binarios  a  bajo  V_DD),  el  binario  suele  ganar  en  área  y  a  menudo  en p roducto energía-retardo. Las 
excep ciones ap arecen cuando el cuello de botella es el número de hilos de un bus o cuando se acep ta 
ap roximación. Esa es una regularidad emp írica de p ap ers de Etiemble y de grup os de CNTFET, no una 
ley de la naturaleza, p ero basta p ara no construir un CPU entero en base 4 . 

6 .4  Cómp uto en memoria  y fotónica  

Arrays memristivos y motores fotónicos han rep ortado energías p or MAC en el rango de décimas de 
p J a unos p ocos p J en condiciones de laboratorio o de modelado de chip , p ara p recisión limitada. Un 
memresonador  III–V  sobre  silicio  ha  mostrado  escrituras  de  0 ,1 5 –0 ,3 6   p J  y  tiemp os  de  cientos  de 

Documento concep tual — sin datos exp erimentales p rop ios  ·  p ágina 1 4  

Lóp ez Paz  ·  Monografía de viabilidad  ·  arq uitectura híbrida  ·  2 0 2 6  

p icosegundos  en  un  disp ositivo  concreto.  Un  motor  fotónico  in-memory  ha  estimado  ~0 ,2   p J/MAC 
bajo  un  conjunto exp lícito de hip ótesis de WDM. Esas cifras justifican la línea 4 .2  como p rograma de 
investigación. No justifican escribir « 0 ,2  p J contra 1  p J»  como resultado de este autor. 

6 .5  Densida d 

La densidad de p uertas lógicas multinivel suele ser p eor, no mejor, q ue la SRAM o el CMOS binario, 
p orq ue  cada  celda  necesita  más  margen  o  más  disp ositivos de referencia. La densidad q ue sí p uede 
mejorar  es la de p esos almacenados p or micrómetro cuadrado en un crossbar, a costa de p recisión y 
de endurance. 

Métrica  de sistema   CMOS binario  de nudo 
compar able   Híbrido pr opues to (tesis B)  Comentario  

Programabilidad general  Alta  Alta en el CPU, baja en el 
array  El OS no se toca 

Energía en GEMM residente  Referencia  Potencialmente menor  Hay que  medirlo con ADC 
Energía en código irregular  Referencia  Igual o peor   El array no ayuda 
Densidad de lógica  Alta  Peor si se insiste en MVL  No compe tir ahí 
Densidad de pesos   SRAM cara  Mejor en RRAM  A costa de variabilidad 
Temper atura  Función de P_dis y del 
paque te  Idéntica función  No hay °C mágicos 

Madurez  Producto  Investigación / pilot o  Esta es la tesis C 

Tabla  3.  Comparación  cualit ativa  de sistema.  No son medidas.  Son juicios de ingeniería  que  el plan  del capítulo  8  debe  poder  
falsar . 

7 . Discusión 

7 .1  Tres tesis 

Tesis  A  —  Reemp lazo  global.  Un  ordenador  no  binario,  de un solo sustrato, q ue sea a la vez más 
ráp ido, más frío, más denso, más barato y comp atible con el software existente, contradice a la vez la 
física  del  ruido,  la  economía  de  las  foundries  y  la  inercia  del  ecosistema.  Esta  tesis  se  considera no 
viable como objetivo de ingeniería de aq uí a q uince años. 

Tesis B — Ventaja energética local. Un acelerador híbrido p ara cargas regulares p uede reducir julios 
p or op eración útil resp ecto a una GPU o un CPU de p rop ósito general en ese kernel. Esto ya ocurre, en 
grados distintos, con TPU, NPU, PIM exp erimental y p rototip os fotónicos. Añadir multinivel dentro de 
la  memoria  y  fotónica  en  el  tejido  de  datos  es  una  extensión  incremental,  no  una  rup tura 
ep istemológica. Esta tesis es viable como p rograma de investigación. 

Tesis  C  —  Sistema  comp leto.  Pasar  de  un  tile  de  laboratorio a un módulo con stack de software, 
yield, calificación de servidor o de borde, y cadena de suministro, es un p roblema de integración de 8  a 
1 5  años y de p resup uesto industrial. No es un p roblema q ue se resuelva con un algoritmo genético de 
5 0 0  generaciones descrito en p seudocódigo. 

7 .2  Comp romisos q ue no desa p a recen 

●  Información p or hilo frente a margen de ruido. 
●  Energía de conmutación frente a tiemp o de ramp a adiabática. 
●  No volatilidad y densidad memristiva frente a endurance y variabilidad. 
●  Ancho de banda fotónico frente a coste de conversión y área de PIC. 

Documento concep tual — sin datos exp erimentales p rop ios  ·  p ágina 1 5  

Lóp ez Paz  ·  Monografía de viabilidad  ·  arq uitectura híbrida  ·  2 0 2 6  

●  Novedad de disp ositivo frente a comp atibilidad con PDK, EDA y comp iladores. 

Un diseño honesto elige un p unto en esa frontera y lo declara. El borrador p revio sugería ganar en 
consumo  y  temp eratura  y,  además,  acercarse  en  frecuencia,  p erdiendo  solo  densidad.  Eso  p uede 
ocurrir en un kernel; no es una ley del disp ositivo. 

7 .3  Softwa re y ecosistema  

Aunq ue  un  laboratorio  mostrara  una  p uerta  1 0   veces  más  eficiente,  un  ordenador  no  existe  sin 
comp ilador, bibliothecas, dep urador, sistema op erativo y p rogramadores. El coste de un ISA nuevo es 
histórico:  se  p aga  en  décadas.  Por  eso  la arq uitectura A es deliberadamente p arásita del ecosistema 
binario. Toda p rop uesta q ue emp iece p or « cambiamos la rep resentación de la información en toda la 
p ila»  está resolviendo el p roblema más caro, no el más físico. 

7 .4  Riesgos 

Riesgo de disp ositivo: q ue los N niveles de la RRAM no sobrevivan a 8 5  °C y a 1 0 ⁷ ciclos con una BER 
comp atible  con  INT8 .  Mitigación:  bajar  N,  p asar  a  PIM  digital  de  1   bit  diferencial,  o  abandonar  el 
multinivel en memoria y conservar solo el in-memory binario. 

Riesgo  de  integración:  q ue  el  ADC,  el  reloj  y  el  control se coman la ventaja del array. Mitigación: 
medir siemp re a nivel de tile, no de celda. 

Riesgo de fotónica: q ue el área y la conversión E/O no comp ensen el cobre en el tamaño de módulo 
q ue el p resup uesto p ermite. Mitigación: criterio de go/no-go al final de la fase 2 . 

Riesgo de software: q ue nadie baje un modelo real. Mitigación: un ingeniero de comp iladores en el 
consorcio desde la fase 0 , no desde la 4 . 

Riesgo  narrativo:  q ue  el  p royecto  se  venda  como  tesis  A  p ara  obtener fondos y se ejecute como 
tesis B. Mitigación: este documento, si se usa, debe circular con las tres tesis a la vista. 

7 .5  Imp lica ciones energética s má s a llá  del chip  

Un acelerador más eficiente no reduce automáticamente la energía de un centro de datos: p uede 
aumentar  la  demanda  (p aradoja  de  Jevons).  El  p lan  no  p romete  un  descenso de la factura eléctrica 
mundial. Promete, si la tesis B se confirma, más op eraciones útiles p or julio en un conjunto de kernels. 
La p olítica energética es otra conversación. 

8 . Pla n de investiga ción y desa rrollo 

Duración  orientativa  de  un  p rograma  de  laboratorio  p úblico-p rivado,  no  de  una  startup   con  un 
único tap -out: 8 –1 4  años. Coste: de unos p ocos millones de euros si se limita a disp ositivos y modelado 
en  consorcio  académico,  a  cientos  de  millones  si  se  p ersigue  un  módulo  calificable  en  foundry.  Las 
cifras  no  son  una  solicitud  de  financiación;  son  una  escala  p ara  no  confundir  un  p ap er  con  un 
p roducto. 
 Documento concep tual — sin datos exp erimentales p rop ios  ·  p ágina 1 6  

Lóp ez Paz  ·  Monografía de viabilidad  ·  arq uitectura híbrida  ·  2 0 2 6  

8 .1  Fa se 0  — Ma rco, ba seline y goberna nza  (6 –1 2  meses) 

Objetivos.  Fijar  kernels,  métricas,  el  CMOS  de  referencia  y  los  PDK  accesibles.  Redactar  un 
documento  de  riesgos  y  una  p olítica  de  p ublicación  de  resultados  negativos.  Contratar  o  asignar  la 
comp etencia de comp ilador. 

Entregables. Banco de p ruebas p úblico (aunq ue sea sintético). Elección documentada de N (niveles 
de RRAM) y de si la fotónica entra o se ap laza. Convenio de foundry o de MPW. 

Criterio de p aso. Existe un baseline contra el q ue se comp arará todo lo demás. Si no se p uede p agar 
un PDK, el p rograma se declara de modelado y no de chip . 

Recursos orientativos. 3 –6  p ersonas; acceso a EDA; 0 ,2 –0 ,8  M€. 

8 .2  Fa se 1  — Disp ositivos elementa les (2 –3  a ños) 

Objetivos.  Elegir  como  máximo  dos  p lataformas:  FET  2 D  o  CMOS  avanzado  de  bajo  V_DD, y una 
RRAM  de  HfOₓ  u  óxido  eq uivalente  en  BEOL.  Caracterizar  niveles,  ruido,  retención,  endurance  y 
disp ersión en array p eq ueño (al menos kilómetros de celda, no una docena). No se « buscan materiales 
con VQE»  como objetivo; se usan DFT/NEGF y caracterización, q ue es lo q ue de verdad usa el camp o. 

Entregables. Informe de disp ositivo con N estados a 8 5  °C y BER acotada, o abandono exp lícito del 
multinivel en lógica y su reserva a memoria. Modelo comp acto usable en SPICE. 

Criterio  de  p aso.  N  ≥  4  estados distinguibles en array a temp eratura de uso, o decisión escrita de 
p asar a PIM de 1 –2  bits. 

Recursos  orientativos.  8 –1 5   p ersonas  entre  disp ositivo  y  medida;  tiemp o  de  sala  blanca  o  de 
p artner; 2 –8  M€ en banda académica, más si hay p roceso p rop io. 

8 .3  Fa se 2  — Circuitos de bloq ue (2 –3  a ños) 

Objetivos. Un MAC memristivo o híbrido, el interfaz binario–multinivel, y un enlace fotónico de tile 
a tile si hay acceso a SiPh. Medir energía p or MAC eq uivalente incluyendo conversiones. 

Entregables.  Tile con cifra desglosada. Informe go/no-go de fotónica. Primer kernel GEMM bajado 
p or el comp ilador, aunq ue sea a mano asistida. 

Criterio de p aso. Ventaja medida frente al baseline de la fase 0  en al menos un kernel, o rediseño. Si 
la ventaja desap arece al incluir ADC, se rediseña el interfaz, no se cambia el titular. 

Recursos orientativos. 1 2 –2 5  p ersonas; uno o dos MPW; 5 –2 0  M€. 

8 .4  Fa se 3  — Integra ción 2 .5 D/3 D y control (2 –3  a ños) 

Objetivos.  Un  módulo  con  CPU  anfitrión,  array  y,  si  se  justificó,  PIC.  Comp ilador  mínimo.  Una 
ap licación de extremo a extremo (una cap a de red o un kernel científico) más eficiente q ue el baseline 
a iso-calidad numérica. 

Entregables. Módulo. Runtime. Informe térmico de p aq uete. Documentación de recalibración. 

Criterio de p aso. La ap licación existe y se p uede enseñar a un revisor externo con scrip ts. 

Recursos orientativos. 2 0 –4 0  p ersonas; ensamblado 2 .5 D; 1 5 –6 0  M€. 

Documento concep tual — sin datos exp erimentales p rop ios  ·  p ágina 1 7  

Lóp ez Paz  ·  Monografía de viabilidad  ·  arq uitectura híbrida  ·  2 0 2 6  

8 .5  Fa se 4  — Fia bilida d, comp a ra ción p ública  y decisión de p roducto (2 –3  a ños) 

Objetivos. Ciclado, retención, EMC, calificación de un p erfil de uso (borde o servidor), y un informe 
negativo  si  la  ventaja  desap arece  a  nivel  de  sistema.  Decisión:  p roducto,  librería  de  IP,  o  cierre 
ordenado. 

Entregables.  Dossier  de  fiabilidad.  Comp aración p ública. Recomendación de industrialización o de 
archivo. 

Recursos orientativos. 2 5 –6 0  p ersonas si hay vía de p roducto; 3 0 –2 0 0  M€ según se p ida o no una 
línea. 

8 .6  Presup uesto p or ba nda s 

Ambición  Años  Orden de magnitud   Qué se obtiene 
Tesis doctoral / lab pequeño   3–4   0,3–1,5  M€  Dispositiv o +  paper , no 
sistema 
Consorcio académico +  
MPW  6–8   5–25  M€  Tile medido y compilador  
mínimo 
Módulo pilot o con partner  
industrial  8–12   40–150  M€  Demostrador de sistema 

Calificación de pr oducto  10–14   150–400  M€+   Algo que  un cliente puede  
compr ar 

Tabla  4.  Bandas  de presupues to. Son órdenes de magnitud  para  no confundir escalas,  no una  partida  presupues taria.  

8 .7  Comp etencia s y goberna nza  

Hacen  falta,  como  mínimo:  disp ositivo  y  p roceso;  circuito  mixto  y  ADC;  fotónica  si  entra; 
microarq uitectura; comp ilador; medida y fiabilidad; y alguien con autoridad p ara cerrar una línea. Un 
comité q ue solo suma ambiciones rep roducirá la tesis A en las notas de p rensa y la B en el laboratorio. 
La gobernanza debe incluir la obligación de p ublicar el no-go. 

8 .8  Corresp ondencia  con la s cinco fa ses del ma nuscrito origina l 

El LaTeX de p artida p rop onía: (1 ) simulación y selección de materiales, 1 –3  años; (2 ) fabricación de 
disp ositivos, 2 –4 ; (3 ) p uertas multinivel, 2 –3 ; (4 ) integración fotónica, 2 –3 ; (5 ) sistema comp leto, 2 –3 . 
Se conserva la duración total. Se inserta una fase 0  de métricas. Se degrada la « selección de materiales 
p or  VQE»   a  caracterización  y  DFT.  Se  p ermite  q ue  la  fotónica  salga  en  la fase 2  si no gana. Se exige 
software  desde el p rincip io. El p resup uesto « cientos de millones»  se reserva a la banda de p roducto, 
no a un estudio concep tual. 

9 . Conclusiones y recomenda ciones 

1 8 . No existe un atajo termodinámico q ue consista en dejar de ser binario. Landauer p or bit no mejora 
con la base. 
1 9 . El límite p ráctico de la lógica de muchos niveles a 3 0 0  K y cap acitances de fF es el ruido, el 
mismatch y el interfaz, no la cota de 1 8  meV. 
2 0 . La vía realista es heterogénea: binario donde hace falta robustez y software; multinivel donde la 
física del disp ositivo ya es analógica (memoria resistiva, p esos fotónicos); fotónica donde el cable 
es el p roblema. 
 Documento concep tual — sin datos exp erimentales p rop ios  ·  p ágina 1 8  

Lóp ez Paz  ·  Monografía de viabilidad  ·  arq uitectura híbrida  ·  2 0 2 6  

2 1 . La p regunta global (« sup erior en velocidad, energía y temp eratura a la vez, en todo el sistema» ) 
tiene, con el conocimiento actual, resp uesta negativa. La p regunta local (« menos julios p or MAC en 
un kernel regular» ) tiene resp uesta abierta y ya p arcialmente afirmativa en la literatura de PIM y 
de fotónica. 
2 2 . La inteligencia artificial es herramienta de diseño y de orq uestación, no un cuarto estado de la 
materia ni un coautor. 
2 3 . Cualq uier cifra de « X veces mejor»  o de « Y p or ciento de p robabilidad de éxito»  q ue no arrastre un 
modelo y un dataset debe omitirse. Este texto las omite a p rop ósito. 
2 4 . El p lan de trabajo debe p oder fracasar en p úblico. Si no p uede, no es un p lan: es un relato. 

Recomendación  p ara  el  autor  y p ara un p osible consorcio: acotar el p rograma a un acelerador de 
ultra-bajo  consumo  p ara  un  conjunto  cerrado  de  kernels,  con  baseline  p úblico  y  sin  narrativa  de 
sustitución del binario. Esa narrativa no resiste la literatura ni la física, y no hace falta p ara justificar el 
trabajo. 

1 0 . Limita ciones de este documento 

●  No hay datos exp erimentales p rop ios. 
●  La selección bibliográfica es rep resentativa, no exhaustiva; el camp o de PIM, SiPh y FET 2 D p ublica 
cada mes. 
●  No se ha firmado acuerdo con ninguna foundry; los p lazos de integración son estimaciones de 
orden de magnitud. 
●  Se han excluido, de forma deliberada, resultados numéricos no rep roducibles del borrador p revio. 
●  No se ha hecho un meta-análisis estadístico de p J/MAC p ublicados; se citan rangos. 
●  El autor no dirige una sala blanca. El documento vale como brújula, no como receta de p roceso. 

1 1 . Autoría , herra mienta s y ética  de cita ción 

Autor.  Lázaro  Lóp ez  Paz:  p lanteamiento  de  la  p regunta,  criterio  editorial  de  esta  revisión  y 
resp onsabilidad del texto. 

Herramientas.  Se  han  usado sistemas de asistencia automática p ara localizar literatura, contrastar 
fórmulas y reescribir el manuscrito. Esas herramientas no son coautoras: no conciben el p roblema, no 
firman  la  ética  de  citación  y  no  p ueden  atribuirse  un  hallazgo  exp erimental.  Nombrar  un  modelo 
concreto como coautor en un estudio de viabilidad da una imp resión de autoridad q ue el modelo no 
tiene. 

Plagio.  No  se  ha  cop iado  el  texto  de  un  p royecto,  tesis  o  artículo  ajeno.  Las  ideas  de  fondo 
p ertenecen  al  acervo  del  camp o  y  se  atribuyen  en  la  sección  1 .6   y  en  las  referencias.  Si  alguna 
formulación  coincidiera  con  un  p ap er  concreto,  debe  considerarse  accidente  de  un  vocabulario 
comp artido y corregirse citando la fuente p rimaria. 

Uso.  Documento  académico  y  concep tual.  No  es  una  oferta  comercial  ni  una  evaluación  de 
inversión. 
 Documento concep tual — sin datos exp erimentales p rop ios  ·  p ágina 1 9  

Lóp ez Paz  ·  Monografía de viabilidad  ·  arq uitectura híbrida  ·  2 0 2 6  

1 2 . Glosa rio 

ADC / DAC. Convertidor analógico-digital y digital-analógico. En un tile memristivo suelen dominar 
área y energía. 

BER. Tasa de error de bit (o de nivel). 

BEOL.  Back  end  of  line:  las  cap as  de  metal  e  isolante  p or  encima  de  los  transistores,  donde  se 
integra a menudo la RRAM. 

GEMM. Producto general de matrices. Kernel dominante de muchas redes y de álgebra densa. 

ISA. Conjunto de instrucciones q ue ve el p rogramador o el comp ilador. 

Landauer (cota de). Energía mínima de borrado irreversible de un bit, k_B T ln 2 . 

MAC. Multip ly-accumulate, la op eración a·b +  c. 

MPW. Multi-p roject wafer: una run de foundry comp artida. 

MVL. Lógica multi-valuada, con más de dos niveles lógicos. 

PCM. Phase-change material, usado en memorias y en p onderación fotónica. 

PDK. Process design kit de una foundry. 

PIM. Processing-in-memory, cómp uto en o junto a la memoria. 

QCA. Quantum-dot cellular automata. 

Quit. Dígito cuaternario, análogo del bit y del trit. 

RRAM. Memoria de conmutación resistiva. 

SiPh. Silicon p hotonics. 

TMD. Dicalcogenuro de metal de transición (MoS₂, WSe₂, …). 

V_DD. Voltaje de alimentación. 

1 3 . Referencia s selecciona da s 

La s entra da s siguientes a ncla n la s a firma ciones del texto. No sustituyen una  revisión sistemá tica . 

●  Landauer, R. (1 9 6 1 ). Irreversibility and heat generation in the comp uting p rocess. IBM J. Res. Dev. 
●  Bennett, C. H. (1 9 7 3 , 1 9 8 2 ). Trabajos fundacionales sobre comp utación lógica reversible. 
●  Toffoli, T.; Fredkin, E. Puertas reversibles. 
●  Bormashenko, E. (2 0 2 0 ). Generalization of the Landauer p rincip le for many-valued logic. Entrop y. 
●  Kycia, R. A. (2 0 2 0 ). An exp lanation of the Landauer bound and its ineffectiveness with regard to multivalued 
logic. 
●  Hayes, B. y literatura de op timal radix. 
●  Etiemble, D. Ternary circuits: why R =  3  is not the op timal radix (arXiv:1 9 0 8 .0 6 8 4 1 ) y comp araciones 
p osteriores de sumadores y multip licadores multi-valuados. 
●  Andreev, M. et al. (2 0 2 2 ). Looking beyond 0  and 1 : p rincip les and technology of multi-valued logic devices. 
Adv. Mater. 
 Documento concep tual — sin datos exp erimentales p rop ios  ·  p ágina 2 0  

Lóp ez Paz  ·  Monografía de viabilidad  ·  arq uitectura híbrida  ·  2 0 2 6  

●  Smith, K. C.; Current, K. W. y la tradición de MVL en IEEE. 
●  Shannon, C. E. (1 9 4 8 ). A mathematical theory of communication. Teorema de Shannon–Hartley. 
●  Chua, L. Memristor. Strukov, D.; Williams, R. S. y la RRAM contemp oránea. 
●  Ielmini, D. et al. HfO₂ RRAM multilevel y neuromórfica (APL Mater. y revisiones IOP). 
●  Xia, Q. y colaboradores. Analog in-memory comp uting con memristores, incluida aritmética científica. 
●  Memresonador III–V/Si: Nature Communications (2 0 2 4 ), doi:1 0 .1 0 3 8 /s4 1 4 6 7 -0 2 4 -4 4 7 7 3 -7 . 
●  Motores fotónicos in-memory y PCM en silicio: trabajos de Oxford, MIT, HP y otros citados en el cap ítulo 3 . 
●  Lent, C. S.; Tougaw, P. D.; Porod, W. Quantum-dot cellular automata. Limitaciones de temp eratura. 
●  Frank, M. P. Adiabatic reversible comp uting. Hanninen, Snider, Lent sobre CMOS adiabático. 
●  Literatura de FET de MoS₂ y vacantes de azufre: ACS Nano, Small, ACS AMI y Nature Communications 
(2 0 1 8 –2 0 2 6 ) sobre p asivación, fiabilidad y lógica 2 D. 
●  Church, G. M.; Goldman, N. et al. (2 0 1 3 ). Towards p ractical, high-cap acity DNA information storage. Nature. 
Contraste de p or q ué el ADN no entra en el p lan de chip . 
●  Brusentsov, N. P. y el comp utador Setun (base 3 ), como antecedente histórico, no como baseline de 2 0 2 6 . 

Anexo A. Cá lculos de a p oyo 

A.1  La nda uer a  3 0 0  K 

k_B  =   1 ,3 8 0 6 4 9 × 1 0 ⁻²³  J/K.  T  =   3 0 0   K.  k_B  T  =   4 ,1 4 1 9 4 7 × 1 0 ⁻²¹  J.  ln  2   ≈  0 ,6 9 3 1 4 7 .  k_B  T  ln  2   =  
2 ,8 7 0 × 1 0 ⁻²¹  J  =   2 ,8 7 0   zJ  ≈  1 7 ,9   meV.  En electronvoltios: 1  eV =  1 ,6 0 2 1 7 6 × 1 0 ⁻¹⁹ J, luego 2 ,8 7 0 × 1 0 ⁻²¹ / 
1 ,6 0 2 1 7 6 × 1 0 ⁻¹⁹ ≈ 0 ,0 1 7 9  eV. 

Para un trit: k_B T ln 3  ≈ 4 ,5 5 × 1 0 ⁻²¹ J ≈ 2 8 ,4  meV. Información del trit: log₂ 3  ≈ 1 ,5 8 5  bits. Cociente: 
2 8 ,4  / 1 ,5 8 5  ≈ 1 7 ,9  meV/bit. Para un q uit: k_B T ln 4  =  2  k_B T ln 2  ≈ 3 5 ,8  meV, y log₂ 4  =  2  bits; otra vez 
1 7 ,9  meV/bit. 

A.2  Ruido kT/C 

σ =  √(k_B T / C). Con C =  1  fF =  1 0 ⁻¹⁵ F: k_B T / C =  4 ,1 4 2 × 1 0 ⁻⁶ V². σ =  2 ,0 3 5 × 1 0 ⁻³ V ≈ 2 ,0 4  mV. Si se 
p ide, p or ejemp lo, 8  σ entre niveles adyacentes, ΔV ≥ 1 6  mV y el número máximo de niveles en 0 ,5 0  V 
es 1  +  0 ,5 0 /0 ,0 1 6  ≈ 3 2 , en el mundo de un solo condensador ideal. El mismatch y el 1 /f recortan ese 
número con dureza. Por eso la tabla 1  del cap ítulo 2  es un techo, no un diseño. 

Si C =  1 0  fF, σ cae a ≈ 0 ,6 4  mV y el techo sube, p ero cargar esos 1 0  fF a 0 ,5 0  V cuesta ½ C V² =  1 ,2 5  fJ 
solo en el escalón, diez veces más q ue con 1  fF. El margen se comp ra con energía. 

A.3  Ra mp a  a dia bá tica  

Para una ramp a lineal de 0  a V en tiemp o τ ap licada a una red RC, la disip ación tiende a (RC/τ) C V² 
cuando τ/RC es grande. Si τ =  1 0  RC, se disip a del orden de una décima de C V² p or transición, frente a 
½ C V² del escalón. El p recio es q ue el reloj duró diez constantes de tiemp o. Multip licar p or la actividad 
y p or el número de nodos da la p otencia. Sin esos tres números no hay « 5 5  °C» . 

A.4  Energía  de un bit CMOS frente a  La nda uer 

½  C  V²  con  C  =  1  fF y V =  0 ,7  V es 2 ,4 5 × 1 0 ⁻¹⁶ J ≈ 8 ,5 × 1 0 ⁴ k_B T ln 2 , cinco órdenes p or encima de 
Landauer. Incluso con C y V menores de un nudo avanzado, el bit lógico sigue lejos de la cota. Por eso 

Documento concep tual — sin datos exp erimentales p rop ios  ·  p ágina 2 1  

Lóp ez Paz  ·  Monografía de viabilidad  ·  arq uitectura híbrida  ·  2 0 2 6  

op timizar  el  radix  p ara  acercarse  a  Landauer  es,  hoy,  resolver  el  p roblema eq uivocado: p rimero hay 
q ue dejar de mover datos y de tirar ½ C V² en cada flanco. 

A.5  Qué ha ría  un VQE bien p la ntea do (y q ué no) 

Un  algoritmo  variacional  cuántico  p uede,  en  p lataformas futuras, estimar estados fundamentales 
de Hamiltonianos de materiales. Un circuito de dos q ubits con cuatro ángulos y un tight-binding 2 × 2  no 
es un descubrimiento de vacantes de azufre en MoS₂. El uso honesto, si algún día el hardware cuántico 
lo  p ermite,  sería  comp arar  defectos  candidatos  contra  DFT  y  contra  EELS  o  STM.  Hasta  entonces, 
DFT/NEGF y la medida mandan. 

Anexo B. Corresp ondencia  con el ma nuscrito origina l en La TeX 

El p unto de p artida fue un artículo en LaTeX titulado « Ordenador No Binario Híbrido de Ultra-Bajo 
Consumo:  Estudio  de  Viabilidad  y  Plan  de  Investigación» ,  firmado p or Lázaro Lóp ez Paz y Deep seek, 
con  fecha  8   de  sep tiembre  de  2 0 2 6 .  Esta  monografía  lo  sustituye.  La  tabla  5   documenta  q ué  se 
conservó, q ué se corrigió y q ué se retiró. 

Bloque  del LaT eX  Destino en esta  monogra fía   Decisión 
Objetivo y alcance  Cap.  1   Conservado y pr ecisado 
Landauer y base b  Cap.  2.1–2.2,  A.1   Conservado; fórmula correcta 
Tabla ΔV/σ  Tabla 1,  A.2   Conservada como aritmética 
pedag ógica 
Capacidad  de canal  Cap.  2.6   Conservada con matices 
«Base  óp tima 3–4»   Cap.  2.7   Rebaja: no es teorema de circuito 
Grafeno 200  000   Cap.  2.8  y 3.4   Corregido a límite vs. dispositiv o 
Tecnologías candidatas  Cap.  3   Ampliadas  con madurez y no-alcance 
Arquit ectura híbrida  Cap.  4.2   Conservada como tesis B 
Reversible / cuántico  Cap.  4.3–4.4   Separ ados del camino crítico 
VQE, GA, Grover, PINN  Cap.  5.5  y A.5   Degradados a herramientas, no 
resultados 
Tablas fJ / °C / 5×   —  Retiradas 
Probabilidades 70  % / 10  %  Cap.  7.1   Sustituidas por  tesis A/B/C 
Plan de 5  fases  Cap.  8   Reordenado con fase 0  y go/no-go 
Deep seek coautor  Cap.  11   Herramienta, no firma 

Tabla  5.  Traz abilidad  entre el LaT eX de partida  y esta  monografía.  

Anexo C. Lista  de comp roba ción p a ra  q uien q uiera  continua r 

2 5 . ¿ Está escrito el kernel y el baseline, con nudo y p recisión?  
2 6 . ¿ La ventaja declarada incluye ADC, p rogramación de p esos, reloj y control?  
2 7 . ¿ Hay datos de array, no de una celda, a la temp eratura de uso?  
2 8 . ¿ El multinivel tiene BER y retención, o solo mesetas en una curva?  
2 9 . ¿ El software baja un modelo real, o solo un GEMM sintético?  
3 0 . ¿ Existe un criterio escrito p ara cancelar la fotónica, el radix o el p royecto?  
3 1 . ¿ Las notas de p rensa describen la tesis B, no la A?  
3 2 . ¿ Las citas ap untan a q uien fabricó el disp ositivo?  
3 3 . ¿ Se p ublicarán también los resultados negativos?  
3 4 . ¿ Alguien del consorcio p uede decir « no»  a un titular?  

— fin de la  monogra fía  — 

Documento concep tual — sin datos exp erimentales p rop ios  ·  p ágina 2 2  
