#!/usr/bin/env python
"""
Demo Interactiva - Mini-Parser
Permite probar el parser de forma interactiva
"""

from mini_parser import MiniParser
from visualizador_arbol import VisualizadorArbol
import sys


def mostrar_menu():
    """Muestra el menú principal"""
    print("\n" + "="*70)
    print("DEMO INTERACTIVA - MINI-PARSER")
    print("="*70)
    print("\nOpciones:")
    print("1. Probar una oración")
    print("2. Ver ejemplos válidos")
    print("3. Ver ejemplos inválidos")
    print("4. Análisis paso a paso (con árbol)")
    print("5. Mostrar gramática")
    print("6. Mostrar vocabulario")
    print("7. Salir")
    print("\nElige una opción (1-7): ", end="")


def mostrar_gramatica():
    """Muestra la gramática soportada"""
    print("\n" + "="*70)
    print("GRAMÁTICA LIBRE DE CONTEXTO")
    print("="*70)
    print("""
Reglas de Producción:

  <oración>     ::= <sujeto> <predicado>
  
  <sujeto>      ::= <artículo> <sustantivo>
                  | <artículo> <sustantivo> <adjetivo>
                  | <artículo> <adjetivo> <sustantivo>
  
  <predicado>   ::= <verbo> <complemento>
  
  <complemento> ::= <artículo> <sustantivo>
                  | <artículo> <sustantivo> <adjetivo>
                  | <artículo> <adjetivo> <sustantivo>

Estructura Básica: SUJETO + VERBO + COMPLEMENTO

Características:
- Patrón SVO (Sujeto-Verbo-Objeto)
- Artículo obligatorio en sujeto y complemento
- Máximo un adjetivo por sintagma nominal
- Adjetivo puede ir antes o después del sustantivo
    """)


def mostrar_vocabulario():
    """Muestra el vocabulario soportado"""
    print("\n" + "="*70)
    print("VOCABULARIO SOPORTADO")
    print("="*70)
    
    from mini_parser import AnalizadorLexico
    lexico = AnalizadorLexico()
    
    print("\n📌 ARTÍCULOS:")
    print("  ", ", ".join(sorted(lexico.articulos)))
    
    print("\n📌 SUSTANTIVOS:")
    sustantivos = sorted(lexico.sustantivos)
    for i in range(0, len(sustantivos), 8):
        print("  ", ", ".join(sustantivos[i:i+8]))
    
    print("\n📌 ADJETIVOS:")
    adjetivos = sorted(lexico.adjetivos)
    for i in range(0, len(adjetivos), 8):
        print("  ", ", ".join(adjetivos[i:i+8]))
    
    print("\n📌 VERBOS:")
    print("  ", ", ".join(sorted(lexico.verbos)))
    
    print(f"\nTotal de palabras: {len(lexico.articulos) + len(lexico.sustantivos) + len(lexico.adjetivos) + len(lexico.verbos)}")


def probar_oracion(parser, oracion):
    """Prueba una oración y muestra resultados"""
    print("\n" + "="*70)
    print(f"ANÁLISIS: '{oracion}'")
    print("="*70)
    
    resultado = parser.analizar(oracion)
    
    # Tokens
    print("\n📋 Tokens:")
    for token in resultado['tokens']:
        if token.tipo.name != 'FIN':
            print(f"  [{token.tipo.value:12}] → '{token.valor}'")
    
    # Resultado
    print("\n🎯 Resultado:")
    if resultado["valido"]:
        print("  ✅ VÁLIDA - La oración cumple con la gramática")
    else:
        print(f"  ❌ INVÁLIDA - Error en fase {resultado['fase']}")
        print("\n📝 Errores:")
        for error in resultado['errores']:
            print(f"  • {error}")


def ejemplos_validos(parser):
    """Muestra ejemplos válidos"""
    print("\n" + "="*70)
    print("EJEMPLOS DE ORACIONES VÁLIDAS")
    print("="*70)
    
    ejemplos = [
        "el perro come un hueso",
        "la niña lee el libro",
        "un gato grande ve la casa",
        "el niño pequeño quiere un libro rojo",
        "los perros buscan las casas",
    ]
    
    for i, ejemplo in enumerate(ejemplos, 1):
        resultado = parser.analizar(ejemplo)
        estado = "✓" if resultado["valido"] else "✗"
        print(f"{i}. {estado} {ejemplo}")


def ejemplos_invalidos(parser):
    """Muestra ejemplos inválidos"""
    print("\n" + "="*70)
    print("EJEMPLOS DE ORACIONES INVÁLIDAS")
    print("="*70)
    
    ejemplos = [
        ("el perro grande", "Falta predicado"),
        ("come el libro", "Falta sujeto"),
        ("el grande perro come libro", "Falta artículo en complemento"),
        ("perro el come un libro", "Orden incorrecto"),
        ("el perro muy grande come el libro", "Palabra 'muy' fuera de vocabulario"),
    ]
    
    for i, (ejemplo, razon) in enumerate(ejemplos, 1):
        resultado = parser.analizar(ejemplo)
        print(f"\n{i}. {ejemplo}")
        print(f"   Razón: {razon}")


def analisis_paso_a_paso(visualizador, oracion):
    """Muestra análisis paso a paso con árbol"""
    print(visualizador.visualizar_pasos(oracion))


def main():
    """Función principal de la demo"""
    parser = MiniParser()
    visualizador = VisualizadorArbol()
    
    print("\n" + "="*70)
    print("¡Bienvenido a la Demo del Mini-Parser!")
    print("="*70)
    print("\nEste parser analiza oraciones simples en español")
    print("con estructura Sujeto-Verbo-Objeto (SVO)")
    
    while True:
        mostrar_menu()
        
        try:
            opcion = input().strip()
            
            if opcion == "1":
                print("\nIngresa una oración (o 'volver' para regresar): ", end="")
                oracion = input().strip()
                if oracion.lower() != 'volver' and oracion:
                    probar_oracion(parser, oracion)
            
            elif opcion == "2":
                ejemplos_validos(parser)
            
            elif opcion == "3":
                ejemplos_invalidos(parser)
            
            elif opcion == "4":
                print("\nIngresa una oración para análisis detallado: ", end="")
                oracion = input().strip()
                if oracion:
                    analisis_paso_a_paso(visualizador, oracion)
            
            elif opcion == "5":
                mostrar_gramatica()
            
            elif opcion == "6":
                mostrar_vocabulario()
            
            elif opcion == "7":
                print("\n¡Gracias por usar el Mini-Parser! 👋\n")
                sys.exit(0)
            
            else:
                print("\n⚠️  Opción inválida. Por favor elige 1-7.")
        
        except KeyboardInterrupt:
            print("\n\n¡Hasta luego! 👋\n")
            sys.exit(0)
        except EOFError:
            print("\n\n¡Hasta luego! 👋\n")
            sys.exit(0)
        
        input("\nPresiona Enter para continuar...")


if __name__ == "__main__":
    main()
