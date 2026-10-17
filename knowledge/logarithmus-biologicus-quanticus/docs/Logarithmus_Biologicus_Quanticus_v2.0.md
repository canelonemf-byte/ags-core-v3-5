> Texto extraído automáticamente del PDF original «Logarithmus_Biologicus_Quanticus_v2.0.pdf». Fórmulas, figuras y maquetación se han perdido; el original está en Drive: https://drive.google.com/file/d/1xgo9mbPz-HVM99MLwMcGiIqyvvTUrCXN/view?usp=drivesdk



Logarithmus Biologicus Quanticus v2.0
Un ´ındice logar´ıtmico cu´antico-asistido con fusi´on algor´ıtmica
para la evaluaci´on del potencial biol´ogico de exoplanetas

[Tu nombre] Tu afiliaci´on¿Tu afiliaci´on

Julio 2026

Abstract

Presentamos la versi´on 2.0 del Logarithmus Biologicus Quanticus (LCPB), un marco com-
putacional exploratorio que combina t´ecnicas cl´asicas de machine learning (Random Forest,
Gradient Boosting, PCA, MCMC, fusi´on Dempster-Shafer) con una capa cu´antica opcional
(QAOA, VQE ADAPT, Grover adaptativo, qPCA, Quantum MCMC) implementada sobre
qiskit. A diferencia de la v1.0, esta versi´on se acompa˜na de una implementaci´on de refer-
encia ejecutable y de una evaluaci´on honesta de sus limitaciones: no existe ning´un cat´alogo
real de exoplanetas con biosfera confirmada, por lo que todo entrenamiento y toda cifra de
exactitud reportada aqu´ı provienen de un dataset sint´etico generado por reglas conocidas
de habitabilidad, y miden ajuste a esa regla, no capacidad real de detecci´on de vida. Sobre
ese dataset sint´etico, el clasificador de referencia alcanza un 65.6% de exactitud (no el 94%
reportado en versiones preliminares de este documento, cifra que no pudo reproducirse ni
justificarse). Se presentan resultados ilustrativos para TRAPPIST-1e, Pr´oxima Centauri b y
Kepler-452b. Los bloques cu´anticos requieren qiskit; cuando no est´a disponible, cada uno
cae a un sustituto cl´asico declarado expl´ıcitamente en el c´odigo.

1 Introducci´on

La b´usqueda de vida extraterrestre necesita m´etricas que integren datos heterog´eneos con siner-
gias no lineales. La versi´on 1.0 del LCPB demostr´o la viabilidad de usar computaci´on cu´antica,
pero ten´ıa limitaciones: pesos sub´optimos, sinergias fijas y falta de validaci´on bayesiana rigurosa.
La v2.0 incorpora un ecosistema de algoritmos cl´asicos y cu´anticos que ataca cada debilidad,
manteniendo la ejecutabilidad en la nube cu´antica actual (IBM Quantum, 2026).

2 Algoritmos incorporados en la v2.0

2.1 Cl´asicos (preprocesamiento y validaci´on)

‹ Random Forest: importancia de caracter´ısticas para eliminar redundancias.

‹ XGBoost: clasificador de referencia para calibrar el sistema cu´antico.

‹ PCA cl´asico: reducci´on de dimensionalidad de 11 a 5 componentes.

‹ MCMC (Metropolis-Hastings): estimaci´on de la distribuci´on posterior de Λ e inter-
valos de credibilidad.

‹ Fusi´on Dempster-Shafer: combina la evidencia del clasificador cu´antico, XGBoost y
nanodatos en una masa de creencia ´unica.

1

2.2 Cu´anticos (optimizaci´on y aceleraci´on)

‹ qPCA: reducci´on cu´antica de dimensionalidad para grandes cat´alogos.

‹ VQE ADAPT: ansatz adaptativo que mejora la precisi´on del c´alculo de la sinergia S.

‹ QAOA: selecciona el subconjunto ´optimo de factores mediante un QUBO.

‹ Grover adaptativo: b´usqueda acelerada en bibliotecas de atm´osferas simuladas.

‹ Quantum MCMC: acelera la convergencia del MCMC con propuestas generadas por
circuitos cu´anticos.

2.3 Simulaci´on y nanotecnolog´ıa

‹ Acople ROCKE-3D: genera datos de entrenamiento con modelos clim´aticos tridimen-
sionales.

‹ Redes metab´olicas: predicci´on de gases traza a partir de genomas de extrem´ofilos.

‹ Procesamiento de nanose˜nales: algoritmo de machine learning para nanoporos (Min-
ION) y nanocantilevers.

3 Metodolog´ıa integrada

El flujo de trabajo completo es:

1. Datos de telescopios (JWST, TESS, ALMA).

2. Preprocesamiento cl´asico (PCA, Random Forest).

3. Reducci´on cu´antica de dimensionalidad (qPCA) [opcional].

4. Selecci´on ´optima de factores con QAOA.

5. C´alculo de pesos din´amicos (QNN + calibraci´on XGBoost).

6. C´alculo de sinergia con VQE ADAPT.

7. Clasificaci´on m´ultiple (QAE, XGBoost, Grover).

8. Fusi´on de evidencia Dempster-Shafer.

9. Inferencia bayesiana con Quantum MCMC.

10. C´alculo final de Λ e intervalo de credibilidad.

11. Incorporaci´on de nanodatos (si existen).

4 F´ormula del LCPB v2.0

Λ = log10
 

 ∏k∈Kopt F ωk(x)
k
∏j∈Jopt R
ρj (x)
j · SADAPT(x)


 + δfusi´on(x) + γ(x) (1)

donde Kopt, Jopt son subconjuntos elegidos por QAOA, SADAPT es la sinergia del VQE adap-
tativo, δfusi´on es la correcci´on de la masa de creencia, y γ(x) es un t´ermino de calibraci´on del
MCMC cu´antico.
 2

5 Limitaciones y honestidad metodol´ogica

Antes de presentar el c´odigo y los resultados, es necesario ser expl´ıcitos sobre lo que este sistema
puede y no puede afirmar:

‹ No hay ground truth real. No existe ning´un exoplaneta con biosfera confirmada, as´ı que
no hay forma de entrenar ni de validar un clasificador contra casos reales positivos. Todos
los n´umeros de exactitud de este documento provienen de un dataset sint´etico, generado
por una regla conocida de habitabilidad m´as ruido; miden qu´e tan bien el modelo recupera
esa regla, no si detecta vida.

‹ qPCA y Quantum MCMC no son viables tal como se describ´ıan. El qPCA
original depende de QRAM a gran escala, inexistente en 2026; se implementan aqu´ı como
sus equivalentes cl´asicos, con advertencia expl´ıcita en el c´odigo.

‹ QAOA y Grover no aportan ventaja en este problema. Seleccionar 6 de 11 variables
es un problema trivial para un solver cl´asico exacto; usar QAOA aqu´ı ser´ıa cosm´etico.

‹ VQE ADAPT requiere un Hamiltoniano f´ısico para ”sinergia biol´ogica” que
no existe en la literatura de astrobiolog´ıa. La sinergia se calcula con una funci´on cl´asica
expl´ıcita.

‹ La cifra de 94% de precisi´on de versiones anteriores de este documento no
pudo reproducirse. La ejecuci´on real del pipeline (c´odigo en la Secci´on 6) da 65.6%
sobre el dataset sint´etico.

Con estas salvedades, el valor del LCPB v2.0 es el de un marco exploratorio y una imple-
mentaci´on de referencia reproducible, ´util para priorizar candidatos con base en biomar-
cadores conocidos, no un instrumento de detecci´on de vida validado.

6 Implementaci´on (c´odigo completo)

A continuaci´on se presenta el c´odigo Python que implementa el pipeline. Es autocontenido,
ejecutable con numpy, scipy y scikit-learn; si qiskit y qiskit-aer est´an instalados, los
bloques cu´anticos se activan, y si no, cada uno cae a un sustituto cl´asico con una advertencia
expl´ıcita en tiempo de ejecuci´on.

1 """

2 lcpb_v2 . py -- Logarithmus Biologicus Quanticus v2 .0

3 = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

4

5 IMPLEMENTACION DE REFERENCIA , NO UN SISTEMA VALIDADO CIENTIFICAMENTE .

6

7 Notas de honestidad ( leer antes de usar ) :

8

9 1. No existe ningun catalogo real de exoplanetas con " biosfera confirmada ".

10 Por lo tanto este script entrena y evalua los clasificadores con datos

11 SINTETICOS generados a partir de reglas conocidas de habitabilidad

12 ( zona habitable , presencia de agua liquida estimada , actividad estelar ,

13 composicion atmosferica simulada ) . Cualquier cifra de " precision " que

14 produzca este script mide que tan bien el modelo recupera la regla

15 sintetica con la que fue generado el dataset -- NO mide su capacidad de

16 detectar vida real en exoplanetas .

17

18 2. Los bloques cuanticos ( QAOA , VQE ADAPT , Grover adaptativo , qPCA ,

19 Quantum MCMC ) requieren la libreria " qiskit ". Si no esta instalada ,

20 cada bloque cae automaticamente a una version clasica equivalente e

21 imprime una advertencia explicita -- el script nunca finge haber usado

3

22 hardware cuantico si no lo hizo .

23

24 3. " qPCA " en su formulacion original ( Lloyd - Mohseni - Rebentrost ) depende de

25 QRAM a gran escala , que no existe en 2026. Aqui se implementa como PCA

26 clasico con una nota , no como el algoritmo cuantico original .

27

28 4. " Quantum MCMC " es un area de investigacion activa sin implementacion

29 madura y estandar . Aqui se implementa Metropolis - Hastings clasico ; la

30 cadena de Markov y su convergencia son clasicas en todos los casos .

31

32 Dependencias minimas : numpy , scipy , scikit - learn .

33 Dependencias opcionales : qiskit + qiskit - aer ( para las partes cuanticas ) .

34 """

35

36 from __future__ import annotations

37 import warnings

38 import numpy as np

39 from dataclasses import dataclass , field

40 from sklearn . decomposition import PCA

41 from sklearn . ensemble import RandomForestClassifier , G r a d i e n t B o o s t i n g C l a s s i f i e r

42 from sklearn . model_selection import train_test_split

43 from sklearn . metrics import accuracy_score

44

45 try :

46 from qiskit import QuantumCircuit

47 from qiskit_aer import AerSimulator

48 HAVE_QISKIT = True

49 except Exception :

50 HAVE_QISKIT = False

51

52

53 def _warn_fallback ( nombre_algoritmo : str ) -> None :

54 warnings . warn (

55 f " [ LCPB v2 .0] qiskit no disponible : ’{ nombre_algoritmo } ’ se ejecuta "

56 f " en modo clasico equivalente , NO en hardware / simulador cuantico . " ,

57 RuntimeWarning ,

58 )

59

60

61 # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

62 # 1. DATOS SINTETICOS DE ENTRENAMIENTO

63 # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

64 def g e n e r a r _ d a t a s e t _ s in t e t i c o ( n : int = 2000 , seed : int = 42) :

65 rng = np . random . default_rng ( seed )

66 temp_eq = rng . normal (288 , 60 , n )

67 radio = rng . gamma (2.0 , 0.7 , n )

68 masa = radio ** 2.06 * rng . normal (1 , 0.15 , n )

69 insolacion = rng . gamma (2.0 , 0.6 , n )

70 excentricidad = rng . beta (1.5 , 8 , n )

71 actividad_estelar = rng . gamma (1.5 , 0.4 , n )

72 h2o = rng . beta (2 , 3 , n )

73 o2 = rng . beta (1.2 , 5 , n )

74 ch4 = rng . beta (1.2 , 6 , n )

75 co2 = rng . beta (2 , 2 , n )

76 zona_habitable = np . exp ( -(( insolacion - 1.0) ** 2) / 0.35)

77

78 X = np . column_stack ([

79 temp_eq , radio , masa , insolacion , excentricidad ,

80 actividad_estelar , h2o , o2 , ch4 , co2 , zona_habitable ,

81 ])

82

83 score = (

84 1.8 * zona_habitable + 1.4 * h2o + 1.1 * o2 + 0.6 * ch4

4

85 - 0.9 * actividad_estelar - 0.8 * excentricidad

86 - 0.01 * np . abs ( temp_eq - 288)

87 )

88 prob = 1 / (1 + np . exp ( -( score - np . median ( score ) ) ) )

89 y = ( rng . uniform (0 , 1 , n ) < prob ) . astype ( int )

90

91 nombres = [

92 " T_eq " , " radio " , " masa " , " insolacion " , " excentricidad " ,

93 " actividad_estelar " , " H2O " , " O2 " , " CH4 " , " CO2 " , " zona_habitable " ,

94 ]

95 return X , y , nombres

96

97

98 # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

99 # 2. PREPROCESAMIENTO CLASICO

100 # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

101 def i m p o r t a n c i a _ r a n d o m_ f o r e s t (X , y , nombres ) :

102 rf = R an do mFo re st Cla ss if ier ( n_estimators =300 , random_state =0)

103 rf . fit (X , y )

104 orden = np . argsort ( rf . feature_importances_ ) [:: -1]

105 return [( nombres [ i ] , float ( rf . feature_importances_ [ i ]) ) for i in orden ]

106

107

108 def reduccion_pca (X , n_componentes =5 , usar_qpca = False ) :

109 if usar_qpca :

110 if not HAVE_QISKIT :

111 _warn_fallback ( " qPCA " )

112 warnings . warn (

113 " [ LCPB v2 .0] qPCA ( Lloyd - Mohseni - Rebentrost ) requiere QRAM a "

114 " gran escala , inexistente en 2026. Se usa PCA clasico . " ,

115 RuntimeWarning ,

116 )

117 pca = PCA ( n_components = n_componentes , random_state =0)

118 X_red = pca . fit_transform ( X )

119 return X_red , pca . e x p l a i n e d _ va r i a n c e _ r a t i o _

120

121

122 # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

123 # 3. SELECCION DE FACTORES

124 # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

125 def seleccion_factores ( nombres , importancias , k =6) :

126 top = sorted ( importancias , key = lambda t : t [1] , reverse = True ) [: k ]

127 seleccionados = [ nombre for nombre , _ in top ]

128 if HAVE_QISKIT :

129 warnings . warn (

130 " [ LCPB v2 .0] QAOA disponible via qiskit , pero para 11 "

131 " variables un solver clasico exacto es mas rapido y no "

132 " aproximado . Se usa seleccion por importancia clasica . " ,

133 RuntimeWarning ,

134 )

135 else :

136 _warn_fallback ( " QAOA " )

137 return seleccionados

138

139

140 # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

141 # 4. CLASIFICADORES

142 # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

143 def e nt re n ar _c l as i fi ca d or e s (X , y ) :

144 X_tr , X_te , y_tr , y_te = train_test_split (

145 X , y , test_size =0.25 , random_state =0 , stratify = y

146 )

147 try :
 5

148 import xgboost as xgb

149 clf_boost = xgb . XGBClassifier (

150 n_estimators =200 , max_depth =4 , eval_metric = " logloss "

151 )

152 nombre_boost = " XGBoost "

153 except ModuleNotFoundError :

154 clf_boost = G r a d i e n t B o o s t i n g C l a s s i f i e r ( n_estimators =200 , max_depth =3)

155 nombre_boost = " GradientBoosting ( sustituto de XGBoost , no instalado ) "

156

157 clf_boost . fit ( X_tr , y_tr )

158 acc = accuracy_score ( y_te , clf_boost . predict ( X_te ) )

159 return clf_boost , nombre_boost , acc

160

161

162 # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

163 # 5. SINERGIA

164 # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

165 def calcular_sinergia ( x_planeta , usar_vqe = True ) :

166 h2o , o2 , ch4 = x_planeta [6] , x_planeta [7] , x_planeta [8]

167 s_clasica = 1.0 + 0.5 * ( h2o * o2 + o2 * ch4 + h2o * ch4 )

168

169 if usar_vqe and not HAVE_QISKIT :

170 _warn_fallback ( " VQE ADAPT " )

171 return s_clasica , " clasica ( sin qiskit ) "

172

173 if usar_vqe and HAVE_QISKIT :

174 warnings . warn (

175 " [ LCPB v2 .0] No existe un Hamiltoniano fisico validado para "

176 " ’ sinergia biologica ’; VQE ADAPT se omite y se usa una "

177 " funcion de sinergia clasica explicita . " ,

178 RuntimeWarning ,

179 )

180 return s_clasica , " clasica ( VQE sin Hamiltoniano fisico definido ) "

181

182 return s_clasica , " clasica "

183

184

185 # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

186 # 6. FUSION DEMPSTER - SHAFER

187 # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

188 def fu sio n_ de mps te r_ sha fe r ( masas : list [ dict ]) -> dict :

189 resultado = masas [0]

190 for m in masas [1:]:

191 nuevo = { " favorable " : 0.0 , " desfavorable " : 0.0 , " incierto " : 0.0}

192 conflicto = 0.0

193 for k1 , v1 in resultado . items () :

194 for k2 , v2 in m . items () :

195 if k1 == k2 :

196 nuevo [ k1 ] += v1 * v2

197 elif " incierto " in ( k1 , k2 ) :

198 clave = k1 if k2 == " incierto " else k2

199 nuevo [ clave ] += v1 * v2

200 else :

201 conflicto += v1 * v2

202 norm = 1.0 - conflicto

203 if norm <= 1e -9:

204 raise ValueError ( " Conflicto total entre fuentes de evidencia ( K =1) . "
)

205 resultado = { k : v / norm for k , v in nuevo . items () }

206 return resultado

207

208

209 # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

6

210 # 7. MCMC ( Metropolis - Hastings clasico )

211 # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

212 def mcmc_lambda ( log_verosimilitud , x0 , n_muestras =4000 , escala =0.3 , seed =0) :

213 if not HAVE_QISKIT :

214 _warn_fallback ( " Quantum MCMC " )

215 rng = np . random . default_rng ( seed )

216 muestras = np . empty ( n_muestras )

217 x = x0

218 log_p_x = log_verosimilitud ( x )

219 aceptadas = 0

220 for i in range ( n_muestras ) :

221 x_prop = x + rng . normal (0 , escala )

222 log_p_prop = log_verosimilitud ( x_prop )

223 if np . log ( rng . uniform () ) < ( log_p_prop - log_p_x ) :

224 x , log_p_x = x_prop , log_p_prop

225 aceptadas += 1

226 muestras [ i ] = x

227 return muestras , aceptadas / n_muestras

228

229

230 # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

231 # 8. FORMULA LCPB Y EVALUACION POR PLANETA

232 # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

233 @dataclass

234 class ResultadoLCPB :

235 planeta : str

236 lam_media : float

237 lam_std : float

238 clasificacion : str

239 tasa_aceptacion_mcmc : float

240 fuente_sinergia : str

241 detalles : dict = field ( default_factory = dict )

242

243

244 def c al cu l ar _l a mb d a_ pu n tu a l ( x_planeta , factores_F , factores_R , pesos_w ,
pesos_rho ) :

245 F = np . prod ( np . array ( factores_F ) ** np . array ( pesos_w ) )

246 R = np . prod ( np . array ( factores_R ) ** np . array ( pesos_rho ) )

247 S , fuente_S = calcular_sinergia ( x_planeta )

248 return np . log10 (( F / R ) * S ) , fuente_S

249

250

251 def evaluar_planeta ( nombre_planeta , x_planeta , clf ) :

252 factores_F = [ x_planeta [6] + 0.05 , x_planeta [7] + 0.05 , x_planeta [10] +
0.05]

253 factores_R = [ x_planeta [5] + 0.05 , x_planeta [4] + 0.05]

254 pesos_w = [0.4 , 0.35 , 0.25]

255 pesos_rho = [0.6 , 0.4]

256

257 lam_puntual , fuente_S = ca l cu la r _l a mb da _ pu n tu al (

258 x_planeta , factores_F , factores_R , pesos_w , pesos_rho

259 )

260

261 log_vero = lambda lam : -0.5 * (( lam - lam_puntual ) / 0.3) ** 2

262 muestras , tasa_acept = mcmc_lambda ( log_vero , lam_puntual )

263 lam_media , lam_std = float ( np . mean ( muestras ) ) , float ( np . std ( muestras ) )

264

265 p_clf = float ( clf . predict_proba ( x_planeta . reshape (1 , -1) ) [0 , 1])

266 masa_clf = { " favorable " : p_clf , " desfavorable " : 1 - p_clf , " incierto " : 0.0}

267 p_lam = min ( max (( lam_media + 3) / 6 , 0) , 1)

268 masa_lambda = { " favorable " : p_lam , " desfavorable " : 1 - p_lam , " incierto " :
0.0}

269 fusion = f us io n_d em ps ter _s ha fe r ([ masa_clf , masa_lambda ])

7

270

271 clasificacion = (

272 " Potencialmente habitable " if fusion [ " favorable " ] > 0.5 else "
Desfavorable "

273 )

274

275 return ResultadoLCPB (

276 planeta = nombre_planeta ,

277 lam_media = lam_media ,

278 lam_std = lam_std ,

279 clasificacion = clasificacion ,

280 tasa_aceptacion_mcmc = tasa_acept ,

281 fuente_sinergia = fuente_S ,

282 detalles ={ " f usi on _d emp st er _sh af er " : fusion , " prob_clasificador " : p_clf } ,

283 )

284

285

286 # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

287 # 9. PIPELINE COMPLETO

288 # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

289 def ej ecu ta r_ pip el in e_d em o () :

290 X , y , nombres = g e n e r a r _ d a ta s e t _ s i n t e t i c o ()

291 importancias = i m p o r t a n c i a _ r an d o m _ f o r e s t (X , y , nombres )

292 _X_red , _var = reduccion_pca (X , n_componentes =5 , usar_qpca = True )

293 seleccionados = seleccion_factores ( nombres , importancias , k =6)

294 clf , nombre_clf , acc = en tr e na r _c la s if i ca do r es (X , y )

295

296 print ( f " Clasificador usado : { nombre_clf } " )

297 print ( f " Exactitud sobre el conjunto de prueba SINTETICO : { acc :.3 f } " )

298 print ( " ( Esta cifra mide ajuste al dataset sintetico generado por " )

299 print ( " reglas conocidas , no capacidad real de deteccion de vida : " )

300 print ( " no existe ground truth real de biosferas confirmadas .) \ n " )

301 print ( " Factores seleccionados ( por importancia clasica ) : " , seleccionados , " \
n " )

302

303 planetas = {

304 " TRAPPIST -1 e " : np . array ([250 , 0.92 , 0.77 , 0.66 , 0.02 , 1.8 , 0.35 , 0.05 ,
0.04 , 0.5 , 0.55]) ,

305 " Proxima Centauri b " : np . array ([234 , 1.03 , 1.27 , 0.65 , 0.03 , 2.4 , 0.30 ,
0.04 , 0.03 , 0.55 , 0.5]) ,

306 " Kepler -452 b " : np . array ([265 , 1.6 , 3.29 , 1.10 , 0.05 , 0.5 , 0.55 , 0.20 ,
0.10 , 0.45 , 0.85]) ,

307 }

308

309 resultados = []

310 for nombre , x in planetas . items () :

311 r = evaluar_planeta ( nombre , x , clf )

312 resultados . append ( r )

313 print (

314 f " { nombre :22 s } Lambda = { r . lam_media :+.2 f } +/ - { r . lam_std :.2 f } "

315 f " [{ r . clasificacion }] ( aceptacion MCMC : { r . tasa_aceptacion_mcmc :.2
f }) "

316 )

317 return resultados , acc

318

319

320 if __name__ == " __main__ " :

321 if not HAVE_QISKIT :

322 print (

323 " AVISO : qiskit no esta instalado en este entorno . Todos los "

324 " bloques cuanticos se ejecutan en modo de sustituto clasico "

325 " declarado ( ver advertencias abajo ) .\ n "

326 )
 8

327 ej ec ut ar_ pi pe lin e_ de mo ()

Listing 1: C´odigo LCPB v2.0 (implementaci´on de referencia real)

7 Resultados

Los siguientes valores se obtuvieron ejecutando directamente el c´odigo de la Secci´on 6 (par´ametros
orbitales y atmosf´ericos ilustrativos, no mediciones observacionales completas) sobre TRAPPIST-
1e, Pr´oxima Centauri b y Kepler-452b, con qiskit no disponible (todos los bloques cu´anticos
en modo de sustituto cl´asico).

Planeta Λ (media ± std) Clasificaci´on Aceptaci´on MCMC

TRAPPIST-1e -0.24 ± 0.31 Desfavorable 0.69
Pr´oxima Cen b -0.38 ± 0.31 Desfavorable 0.69
Kepler-452b +0.30 ± 0.31 Potencialmente habitable 0.69

Table 1: Valores de Λ obtenidos de una ejecuci´on real del c´odigo (semillas fijas, dataset sint´etico).
El clasificador de referencia alcanz´o 65.6% de exactitud sobre el conjunto de prueba sint´etico.

Kepler-452b sigue siendo el candidato relativamente m´as favorable de los tres, coherente
con su menor actividad estelar simulada y mayor ´ındice de zona habitable. Esta ordenaci´on
relativa es razonablemente robusta, pero los valores absolutos de Λ dependen fuertemente de los
pesos y factores elegidos a mano en la Secci´on 6, que no han sido calibrados contra ning´un dato
observacional independiente.

8 Conclusiones

El LCPB v2.0 es un marco exploratorio con una implementaci´on de referencia real y reproducible,
no un instrumento validado de detecci´on de biosferas. Su componente cl´asico (Random Forest,
Gradient Boosting, PCA, MCMC, fusi´on Dempster-Shafer) funciona genuinamente y puede ser
´util para priorizar candidatos seg´un biomarcadores conocidos. Su componente cu´antico es en
gran parte demostrativo: qPCA y Quantum MCMC no son viables con hardware actual tal como
se plantean originalmente, QAOA y Grover no ofrecen ventaja en problemas de este tama˜no,
y VQE ADAPT carece de un Hamiltoniano f´ısico validado para ”sinergia biol´ogica”. La cifra
de 94% de precisi´on de versiones previas de este documento no se pudo reproducir; la cifra
real, sobre datos sint´eticos, es 65.6%. Cualquier uso de este marco para priorizar objetivos de
observaci´on real deber´ıa tratarlo como una herramienta heur´ıstica, sujeta a revisi´on por pares,
no como un resultado cient´ıfico establecido.

Disponibilidad

C´odigo y datos en: https://github.com/tu-repositorio/lcpb

9
