"""
Comparación entre Parser Manual vs Modelo NLP Moderno
Contraste de desempeño: Parser Descendente Recursivo vs spaCy (Deep Learning)
"""

import time
from typing import List, Dict
from mini_parser import MiniParser


def verificar_dependencias():
    """Verifica que spaCy esté disponible"""
    try:
        import spacy
        nlp = spacy.load("es_core_news_sm")
        print("✓ spaCy y modelo es_core_news_sm disponibles")
        return True
    except Exception as e:
        print(f"✗ Error al cargar spaCy: {e}")
        return False


class AnalizadorNLPModerno:
    """Wrapper para análisis con spaCy (modelo estadístico/deep learning)"""
    
    def __init__(self):
        import spacy
        self.nlp = spacy.load("es_core_news_sm")
    
    def analizar(self, texto: str) -> dict:
        """
        Analiza texto usando spaCy (modelo basado en redes neuronales)
        
        Returns:
            Diccionario con análisis sintáctico y POS tagging
        """
        inicio = time.time()
        doc = self.nlp(texto)
        tiempo = time.time() - inicio
        
        # Extraer información
        tokens = []
        for token in doc:
            tokens.append({
                "texto": token.text,
                "pos": token.pos_,  # Part-of-Speech tag
                "tag": token.tag_,  # Etiqueta detallada
                "dep": token.dep_,  # Dependencia sintáctica
                "lemma": token.lemma_,
                "es_stop": token.is_stop
            })
        
        # Verificar estructura SVO (Sujeto-Verbo-Objeto)
        tiene_sujeto = any(t["dep"] in ["nsubj", "nsubj:pass"] for t in tokens)
        tiene_verbo = any(t["pos"] == "VERB" for t in tokens)
        tiene_objeto = any(t["dep"] in ["obj", "dobj", "iobj"] for t in tokens)
        
        estructura_svo = tiene_sujeto and tiene_verbo and tiene_objeto
        
        return {
            "texto": texto,
            "tokens": tokens,
            "num_tokens": len(tokens),
            "tiene_sujeto": tiene_sujeto,
            "tiene_verbo": tiene_verbo,
            "tiene_objeto": tiene_objeto,
            "estructura_svo": estructura_svo,
            "tiempo_ms": tiempo * 1000
        }


class ComparadorParsers:
    """Compara el desempeño de ambos parsers"""
    
    def __init__(self):
        self.parser_manual = MiniParser()
        self.parser_nlp = AnalizadorNLPModerno()
    
    def comparar(self, casos_prueba: List[str]) -> Dict:
        """
        Compara ambos parsers con múltiples casos de prueba
        
        Returns:
            Diccionario con estadísticas comparativas
        """
        resultados = {
            "casos": [],
            "stats_manual": {
                "validos": 0,
                "invalidos": 0,
                "tiempo_total": 0,
                "errores_lexico": 0,
                "errores_sintactico": 0
            },
            "stats_nlp": {
                "con_estructura_svo": 0,
                "sin_estructura_svo": 0,
                "tiempo_total": 0
            }
        }
        
        for caso in casos_prueba:
            # Parser manual
            inicio = time.time()
            resultado_manual = self.parser_manual.analizar(caso)
            tiempo_manual = (time.time() - inicio) * 1000
            
            # Parser NLP
            resultado_nlp = self.parser_nlp.analizar(caso)
            
            # Acumular estadísticas
            if resultado_manual["valido"]:
                resultados["stats_manual"]["validos"] += 1
            else:
                resultados["stats_manual"]["invalidos"] += 1
                if resultado_manual["fase"] == "léxico":
                    resultados["stats_manual"]["errores_lexico"] += 1
                else:
                    resultados["stats_manual"]["errores_sintactico"] += 1
            
            resultados["stats_manual"]["tiempo_total"] += tiempo_manual
            
            if resultado_nlp["estructura_svo"]:
                resultados["stats_nlp"]["con_estructura_svo"] += 1
            else:
                resultados["stats_nlp"]["sin_estructura_svo"] += 1
            
            resultados["stats_nlp"]["tiempo_total"] += resultado_nlp["tiempo_ms"]
            
            # Guardar resultado individual
            resultados["casos"].append({
                "texto": caso,
                "manual": {
                    "valido": resultado_manual["valido"],
                    "fase": resultado_manual.get("fase", "N/A"),
                    "tiempo_ms": tiempo_manual
                },
                "nlp": {
                    "estructura_svo": resultado_nlp["estructura_svo"],
                    "tiene_sujeto": resultado_nlp["tiene_sujeto"],
                    "tiene_verbo": resultado_nlp["tiene_verbo"],
                    "tiene_objeto": resultado_nlp["tiene_objeto"],
                    "tiempo_ms": resultado_nlp["tiempo_ms"],
                    "pos_tags": [f"{t['texto']}:{t['pos']}" for t in resultado_nlp["tokens"]]
                }
            })
        
        return resultados
    
    def mostrar_comparacion_detallada(self, resultados: Dict):
        """Muestra una comparación detallada de los resultados"""
        print("\n" + "="*80)
        print("COMPARACIÓN DETALLADA: PARSER MANUAL VS NLP MODERNO")
        print("="*80)
        
        for i, caso in enumerate(resultados["casos"], 1):
            print(f"\n{'─'*80}")
            print(f"Caso {i}: \"{caso['texto']}\"")
            print(f"{'─'*80}")
            
            # Resultado parser manual
            print(f"\n📋 PARSER MANUAL (Gramática Formal):")
            if caso["manual"]["valido"]:
                print(f"   ✓ VÁLIDO - Cumple gramática SVO definida")
            else:
                print(f"   ✗ INVÁLIDO - Error en fase {caso['manual']['fase']}")
            print(f"   ⏱ Tiempo: {caso['manual']['tiempo_ms']:.4f} ms")
            
            # Resultado NLP
            print(f"\n🤖 PARSER NLP (spaCy - Deep Learning):")
            print(f"   Estructura SVO detectada: {'✓ Sí' if caso['nlp']['estructura_svo'] else '✗ No'}")
            print(f"   • Sujeto: {'✓' if caso['nlp']['tiene_sujeto'] else '✗'}")
            print(f"   • Verbo: {'✓' if caso['nlp']['tiene_verbo'] else '✗'}")
            print(f"   • Objeto: {'✓' if caso['nlp']['tiene_objeto'] else '✗'}")
            print(f"   ⏱ Tiempo: {caso['nlp']['tiempo_ms']:.4f} ms")
            print(f"   POS Tags: {' '.join(caso['nlp']['pos_tags'][:10])}")
        
        # Resumen estadístico
        print(f"\n\n{'='*80}")
        print("RESUMEN ESTADÍSTICO")
        print(f"{'='*80}")
        
        total_casos = len(resultados["casos"])
        stats_m = resultados["stats_manual"]
        stats_n = resultados["stats_nlp"]
        
        print(f"\n📊 PARSER MANUAL:")
        print(f"   • Oraciones válidas: {stats_m['validos']}/{total_casos} "
              f"({stats_m['validos']/total_casos*100:.1f}%)")
        print(f"   • Oraciones inválidas: {stats_m['invalidos']}/{total_casos} "
              f"({stats_m['invalidos']/total_casos*100:.1f}%)")
        print(f"     - Errores léxicos: {stats_m['errores_lexico']}")
        print(f"     - Errores sintácticos: {stats_m['errores_sintactico']}")
        print(f"   • Tiempo total: {stats_m['tiempo_total']:.4f} ms")
        print(f"   • Tiempo promedio: {stats_m['tiempo_total']/total_casos:.4f} ms/oración")
        
        print(f"\n🤖 PARSER NLP (spaCy):")
        print(f"   • Con estructura SVO: {stats_n['con_estructura_svo']}/{total_casos} "
              f"({stats_n['con_estructura_svo']/total_casos*100:.1f}%)")
        print(f"   • Sin estructura SVO: {stats_n['sin_estructura_svo']}/{total_casos} "
              f"({stats_n['sin_estructura_svo']/total_casos*100:.1f}%)")
        print(f"   • Tiempo total: {stats_n['tiempo_total']:.4f} ms")
        print(f"   • Tiempo promedio: {stats_n['tiempo_total']/total_casos:.4f} ms/oración")
        
        # Análisis comparativo
        print(f"\n\n{'='*80}")
        print("ANÁLISIS COMPARATIVO")
        print(f"{'='*80}")
        
        velocidad_ratio = stats_m['tiempo_total'] / stats_n['tiempo_total']
        
        print(f"\n⚡ DESEMPEÑO:")
        if velocidad_ratio < 1:
            print(f"   • Parser Manual es {1/velocidad_ratio:.2f}x más rápido que spaCy")
        else:
            print(f"   • spaCy es {velocidad_ratio:.2f}x más rápido que Parser Manual")
        
        print(f"\n🎯 PRECISIÓN:")
        print(f"   • Parser Manual: Verifica gramática formal estricta (SVO con vocabulario limitado)")
        print(f"   • spaCy: Identifica dependencias sintácticas en lenguaje natural general")
        
        print(f"\n📝 FORTALEZAS Y DEBILIDADES:")
        print(f"\n   Parser Manual:")
        print(f"   ✓ Extremadamente rápido")
        print(f"   ✓ Reglas explícitas y comprensibles")
        print(f"   ✓ Ideal para lenguajes de dominio específico")
        print(f"   ✗ Vocabulario muy limitado")
        print(f"   ✗ No maneja variaciones del lenguaje natural")
        print(f"   ✗ Requiere mantenimiento manual de reglas")
        
        print(f"\n   Parser NLP (spaCy):")
        print(f"   ✓ Maneja vocabulario ilimitado")
        print(f"   ✓ Robusto ante variaciones lingüísticas")
        print(f"   ✓ Pre-entrenado en corpus masivos")
        print(f"   ✓ Identifica entidades, lemas, dependencias")
        print(f"   ✗ Más lento (requiere inferencia neural)")
        print(f"   ✗ Menos interpretable (caja negra)")
        print(f"   ✗ Requiere recursos computacionales mayores")
        
        print(f"\n{'='*80}\n")


def main():
    """Función principal"""
    print("="*80)
    print("VERIFICACIÓN DE DEPENDENCIAS")
    print("="*80)
    if not verificar_dependencias():
        return
    
    print("\n\n" + "="*80)
    print("FASE 2: COMPARACIÓN DE PARSERS")
    print("Parser Descendente Recursivo vs Modelo NLP Moderno (spaCy)")
    print("="*80)
    
    # Casos de prueba diversos
    casos_prueba = [
        # Válidos para gramática estricta
        "el perro come un hueso",
        "la niña lee el libro",
        "un gato grande ve la casa",
        "el niño pequeño quiere un libro rojo",
        
        # Inválidos para gramática (pero válidos en español)
        "el perro come",  # Sin complemento
        "come el libro",  # Sin sujeto explícito
        "el grande perro come libro",  # Sin artículo en complemento
        
        # Vocabulario fuera de la gramática
        "el estudiante estudia matemáticas",
        "python es un lenguaje de programación",
        "la inteligencia artificial avanza rápidamente",
        
        # Estructuras más complejas
        "el perro muy grande come el libro azul",
        "los gatos negros cazan ratones pequeños",
    ]
    
    # Ejecutar comparación
    comparador = ComparadorParsers()
    resultados = comparador.comparar(casos_prueba)
    
    # Mostrar resultados
    comparador.mostrar_comparacion_detallada(resultados)


if __name__ == "__main__":
    main()
