"""
Visualizador de Árboles de Parsing
Genera visualización del proceso de análisis sintáctico
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from mini_parser import MiniParser, AnalizadorLexico, TipoToken


@dataclass
class NodoArbol:
    """Representa un nodo en el árbol de parsing"""
    simbolo: str
    hijos: List['NodoArbol']
    token: Optional[str] = None
    nivel: int = 0


class VisualizadorArbol:
    """Visualiza el árbol de análisis sintáctico"""
    
    def __init__(self):
        self.parser = MiniParser()
        self.lexico = AnalizadorLexico()
    
    def construir_arbol(self, texto: str) -> Optional[NodoArbol]:
        """
        Construye el árbol de derivación para una oración
        """
        resultado = self.parser.analizar(texto)
        
        if not resultado["valido"]:
            return None
        
        tokens = resultado["tokens"]
        return self._construir_arbol_recursivo(tokens)
    
    def _construir_arbol_recursivo(self, tokens: List) -> NodoArbol:
        """Construye árbol recursivamente"""
        # Raíz
        raiz = NodoArbol("ORACIÓN", [], nivel=0)
        
        # Separar sujeto y predicado
        pos_verbo = next((i for i, t in enumerate(tokens) if t.tipo == TipoToken.VERBO), -1)
        
        if pos_verbo == -1:
            return raiz
        
        tokens_sujeto = tokens[:pos_verbo]
        tokens_predicado = tokens[pos_verbo:]
        
        # Construir sujeto
        sujeto = self._construir_sujeto(tokens_sujeto)
        sujeto.nivel = 1
        raiz.hijos.append(sujeto)
        
        # Construir predicado
        predicado = self._construir_predicado(tokens_predicado)
        predicado.nivel = 1
        raiz.hijos.append(predicado)
        
        return raiz
    
    def _construir_sujeto(self, tokens: List) -> NodoArbol:
        """Construye nodo del sujeto"""
        sujeto = NodoArbol("SUJETO", [])
        
        for token in tokens:
            if token.tipo == TipoToken.FIN:
                continue
            
            tipo_map = {
                TipoToken.ARTICULO: "ARTÍCULO",
                TipoToken.SUSTANTIVO: "SUSTANTIVO",
                TipoToken.ADJETIVO: "ADJETIVO"
            }
            
            nodo = NodoArbol(
                tipo_map.get(token.tipo, "DESCONOCIDO"),
                [],
                token.valor,
                nivel=2
            )
            sujeto.hijos.append(nodo)
        
        return sujeto
    
    def _construir_predicado(self, tokens: List) -> NodoArbol:
        """Construye nodo del predicado"""
        predicado = NodoArbol("PREDICADO", [])
        
        # Primero el verbo
        if tokens and tokens[0].tipo == TipoToken.VERBO:
            verbo = NodoArbol("VERBO", [], tokens[0].valor, nivel=2)
            predicado.hijos.append(verbo)
            tokens = tokens[1:]
        
        # Luego el complemento
        if tokens:
            complemento = NodoArbol("COMPLEMENTO", [], nivel=2)
            
            for token in tokens:
                if token.tipo == TipoToken.FIN:
                    continue
                
                tipo_map = {
                    TipoToken.ARTICULO: "ARTÍCULO",
                    TipoToken.SUSTANTIVO: "SUSTANTIVO",
                    TipoToken.ADJETIVO: "ADJETIVO"
                }
                
                nodo = NodoArbol(
                    tipo_map.get(token.tipo, "DESCONOCIDO"),
                    [],
                    token.valor,
                    nivel=3
                )
                complemento.hijos.append(nodo)
            
            predicado.hijos.append(complemento)
        
        return predicado
    
    def visualizar_ascii(self, nodo: NodoArbol, prefijo: str = "", es_ultimo: bool = True) -> str:
        """
        Genera representación ASCII del árbol
        """
        resultado = []
        
        # Símbolo del nodo
        conector = "└── " if es_ultimo else "├── "
        simbolo = f"{nodo.simbolo}"
        if nodo.token:
            simbolo += f': "{nodo.token}"'
        
        if nodo.nivel == 0:
            resultado.append(simbolo)
        else:
            resultado.append(prefijo + conector + simbolo)
        
        # Hijos
        for i, hijo in enumerate(nodo.hijos):
            es_ultimo_hijo = (i == len(nodo.hijos) - 1)
            extension = "    " if es_ultimo else "│   "
            nuevo_prefijo = prefijo + extension if nodo.nivel > 0 else ""
            resultado.append(self.visualizar_ascii(hijo, nuevo_prefijo, es_ultimo_hijo))
        
        return "\n".join(resultado)
    
    def visualizar_pasos(self, texto: str) -> str:
        """
        Muestra paso a paso el proceso de parsing
        """
        resultado = []
        resultado.append("="*70)
        resultado.append(f"ANÁLISIS PASO A PASO: '{texto}'")
        resultado.append("="*70)
        
        # Paso 1: Tokenización
        resultado.append("\n📍 PASO 1: ANÁLISIS LÉXICO (Tokenización)")
        resultado.append("-"*70)
        tokens = self.lexico.tokenizar(texto)
        
        for i, token in enumerate(tokens[:-1]):  # Excluir token FIN
            resultado.append(f"  Token {i+1}: [{token.tipo.value:12}] → '{token.valor}'")
        
        # Paso 2: Análisis sintáctico
        resultado.append("\n📍 PASO 2: ANÁLISIS SINTÁCTICO")
        resultado.append("-"*70)
        
        analisis = self.parser.analizar(texto)
        
        if analisis["valido"]:
            resultado.append("  ✓ La oración es sintácticamente válida")
            resultado.append("\n  Reglas aplicadas:")
            resultado.append("  1. <oración> → <sujeto> <predicado>")
            
            # Detectar estructura del sujeto
            tokens_validos = [t for t in tokens if t.tipo != TipoToken.FIN]
            pos_verbo = next((i for i, t in enumerate(tokens_validos) if t.tipo == TipoToken.VERBO), -1)
            
            if pos_verbo > 0:
                tokens_sujeto = tokens_validos[:pos_verbo]
                tiene_adjetivo = any(t.tipo == TipoToken.ADJETIVO for t in tokens_sujeto)
                
                if tiene_adjetivo:
                    resultado.append("  2. <sujeto> → <artículo> [<adjetivo>] <sustantivo>")
                else:
                    resultado.append("  2. <sujeto> → <artículo> <sustantivo>")
                
                resultado.append("  3. <predicado> → <verbo> <complemento>")
                
                # Detectar estructura del complemento
                tokens_complemento = tokens_validos[pos_verbo+1:]
                tiene_adj_comp = any(t.tipo == TipoToken.ADJETIVO for t in tokens_complemento)
                
                if tiene_adj_comp:
                    resultado.append("  4. <complemento> → <artículo> [<adjetivo>] <sustantivo>")
                else:
                    resultado.append("  4. <complemento> → <artículo> <sustantivo>")
        else:
            resultado.append(f"  ✗ La oración NO es válida")
            resultado.append(f"  Fase de error: {analisis['fase']}")
            resultado.append("\n  Errores detectados:")
            for error in analisis['errores']:
                resultado.append(f"    • {error}")
        
        # Paso 3: Árbol de derivación
        if analisis["valido"]:
            resultado.append("\n📍 PASO 3: ÁRBOL DE DERIVACIÓN")
            resultado.append("-"*70)
            arbol = self.construir_arbol(texto)
            if arbol:
                resultado.append(self.visualizar_ascii(arbol))
        
        resultado.append("\n" + "="*70)
        return "\n".join(resultado)


def main():
    """Función principal con ejemplos"""
    visualizador = VisualizadorArbol()
    
    print("\n" + "="*70)
    print("VISUALIZADOR DE ÁRBOLES DE PARSING")
    print("="*70)
    
    casos = [
        "el perro come un hueso",
        "la niña pequeña lee el libro rojo",
        "un gato ve la casa",
        "el perro grande",  # Inválido
    ]
    
    for caso in casos:
        print(visualizador.visualizar_pasos(caso))
        print("\n")


if __name__ == "__main__":
    main()
