"""
Mini-Parser para Lenguaje Natural Limitado
Implementación de parser descendente recursivo con gramática libre de contexto
"""

from typing import List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class TipoToken(Enum):
    """Tipos de tokens reconocidos por el analizador léxico"""
    ARTICULO = "ARTICULO"
    SUSTANTIVO = "SUSTANTIVO"
    ADJETIVO = "ADJETIVO"
    VERBO = "VERBO"
    FIN = "FIN"
    DESCONOCIDO = "DESCONOCIDO"


@dataclass
class Token:
    """Representa un token con su tipo y valor"""
    tipo: TipoToken
    valor: str
    posicion: int


class AnalizadorLexico:
    """Analizador léxico - convierte texto en tokens"""
    
    def __init__(self):
        # Vocabulario definido por la gramática
        self.articulos = {"el", "la", "un", "una", "los", "las"}
        self.sustantivos = {
            "perro", "perros", "gato", "gatos", "niño", "niña", "niños", "niñas",
            "casa", "casas", "libro", "libros", "árbol", "árboles",
            "computadora", "computadoras", "carro", "carros", "hueso", "huesos"
        }
        self.adjetivos = {
            "grande", "grandes", "pequeño", "pequeña", "pequeños", "pequeñas",
            "rojo", "roja", "rojos", "rojas",
            "azul", "azules", "hermoso", "hermosa", "hermosos", "hermosas",
            "viejo", "vieja", "viejos", "viejas",
            "nuevo", "nueva", "nuevos", "nuevas",
            "rápido", "rápida", "rápidos", "rápidas"
        }
        self.verbos = {
            "come", "comen", "lee", "leen", "ve", "ven", "quiere", "quieren",
            "tiene", "tienen", "busca", "buscan", "escribe", "escriben",
            "maneja", "manejan"
        }
    
    def tokenizar(self, texto: str) -> List[Token]:
        """
        Convierte una cadena de texto en una lista de tokens
        
        Args:
            texto: Cadena a tokenizar
            
        Returns:
            Lista de tokens identificados
        """
        palabras = texto.lower().strip().split()
        tokens = []
        
        for i, palabra in enumerate(palabras):
            if palabra in self.articulos:
                tokens.append(Token(TipoToken.ARTICULO, palabra, i))
            elif palabra in self.sustantivos:
                tokens.append(Token(TipoToken.SUSTANTIVO, palabra, i))
            elif palabra in self.adjetivos:
                tokens.append(Token(TipoToken.ADJETIVO, palabra, i))
            elif palabra in self.verbos:
                tokens.append(Token(TipoToken.VERBO, palabra, i))
            else:
                tokens.append(Token(TipoToken.DESCONOCIDO, palabra, i))
        
        # Token de fin
        tokens.append(Token(TipoToken.FIN, "", len(palabras)))
        return tokens


class ParserDescendenteRecursivo:
    """
    Parser descendente recursivo para la gramática definida
    
    Gramática:
        <oración> ::= <sujeto> <predicado>
        <sujeto> ::= <artículo> <sustantivo> | <artículo> <adjetivo> <sustantivo>
        <predicado> ::= <verbo> <complemento>
        <complemento> ::= <artículo> <sustantivo> | <artículo> <adjetivo> <sustantivo>
    """
    
    def __init__(self):
        self.tokens: List[Token] = []
        self.posicion = 0
        self.errores: List[str] = []
    
    def token_actual(self) -> Token:
        """Retorna el token en la posición actual"""
        if self.posicion < len(self.tokens):
            return self.tokens[self.posicion]
        return Token(TipoToken.FIN, "", self.posicion)
    
    def avanzar(self):
        """Avanza a la siguiente posición"""
        if self.posicion < len(self.tokens) - 1:
            self.posicion += 1
    
    def coincidir(self, tipo_esperado: TipoToken) -> bool:
        """
        Verifica si el token actual coincide con el tipo esperado
        
        Args:
            tipo_esperado: Tipo de token que se espera
            
        Returns:
            True si coincide, False en caso contrario
        """
        if self.token_actual().tipo == tipo_esperado:
            self.avanzar()
            return True
        
        self.errores.append(
            f"Error en posición {self.posicion}: "
            f"Se esperaba {tipo_esperado.value}, "
            f"pero se encontró {self.token_actual().tipo.value} ('{self.token_actual().valor}')"
        )
        return False
    
    def parsear_oracion(self) -> bool:
        """
        <oración> ::= <sujeto> <predicado>
        """
        return self.parsear_sujeto() and self.parsear_predicado()
    
    def parsear_sujeto(self) -> bool:
        """
        <sujeto> ::= <artículo> <sustantivo> | <artículo> <adjetivo> <sustantivo> 
                    | <artículo> <sustantivo> <adjetivo>
        
        Permite adjetivos antes o después del sustantivo (como en español)
        """
        if not self.coincidir(TipoToken.ARTICULO):
            return False
        
        # Caso 1: artículo + adjetivo + sustantivo (el grande perro)
        if self.token_actual().tipo == TipoToken.ADJETIVO:
            if not self.coincidir(TipoToken.ADJETIVO):
                return False
            return self.coincidir(TipoToken.SUSTANTIVO)
        
        # Caso 2: artículo + sustantivo [+ adjetivo opcional] (el perro [grande])
        if not self.coincidir(TipoToken.SUSTANTIVO):
            return False
        
        # Adjetivo después del sustantivo es opcional
        if self.token_actual().tipo == TipoToken.ADJETIVO:
            self.coincidir(TipoToken.ADJETIVO)
        
        return True
    
    def parsear_predicado(self) -> bool:
        """
        <predicado> ::= <verbo> <complemento>
        """
        if not self.coincidir(TipoToken.VERBO):
            return False
        
        return self.parsear_complemento()
    
    def parsear_complemento(self) -> bool:
        """
        <complemento> ::= <artículo> <sustantivo> | <artículo> <adjetivo> <sustantivo>
                         | <artículo> <sustantivo> <adjetivo>
        
        Permite adjetivos antes o después del sustantivo (como en español)
        """
        if not self.coincidir(TipoToken.ARTICULO):
            return False
        
        # Caso 1: artículo + adjetivo + sustantivo (un grande libro)
        if self.token_actual().tipo == TipoToken.ADJETIVO:
            if not self.coincidir(TipoToken.ADJETIVO):
                return False
            return self.coincidir(TipoToken.SUSTANTIVO)
        
        # Caso 2: artículo + sustantivo [+ adjetivo opcional] (un libro [rojo])
        if not self.coincidir(TipoToken.SUSTANTIVO):
            return False
        
        # Adjetivo después del sustantivo es opcional
        if self.token_actual().tipo == TipoToken.ADJETIVO:
            self.coincidir(TipoToken.ADJETIVO)
        
        return True
    
    def parsear(self, tokens: List[Token]) -> Tuple[bool, List[str]]:
        """
        Método principal de parsing
        
        Args:
            tokens: Lista de tokens a parsear
            
        Returns:
            Tupla (éxito, lista_de_errores)
        """
        self.tokens = tokens
        self.posicion = 0
        self.errores = []
        
        exito = self.parsear_oracion()
        
        # Verificar que hayamos llegado al final
        if exito and self.token_actual().tipo != TipoToken.FIN:
            self.errores.append(
                f"Error: Tokens adicionales después del final de la oración: "
                f"'{self.token_actual().valor}'"
            )
            exito = False
        
        return exito, self.errores


class MiniParser:
    """Interfaz principal del mini-parser"""
    
    def __init__(self):
        self.lexico = AnalizadorLexico()
        self.parser = ParserDescendenteRecursivo()
    
    def analizar(self, texto: str) -> dict:
        """
        Analiza una cadena de texto completa
        
        Args:
            texto: Texto a analizar
            
        Returns:
            Diccionario con resultados del análisis
        """
        # Análisis léxico
        tokens = self.lexico.tokenizar(texto)
        
        # Verificar tokens desconocidos
        tokens_desconocidos = [t for t in tokens if t.tipo == TipoToken.DESCONOCIDO]
        
        if tokens_desconocidos:
            return {
                "valido": False,
                "fase": "léxico",
                "texto": texto,
                "tokens": tokens,
                "errores": [f"Palabra desconocida: '{t.valor}'" for t in tokens_desconocidos]
            }
        
        # Análisis sintáctico
        exito, errores = self.parser.parsear(tokens)
        
        return {
            "valido": exito,
            "fase": "sintáctico" if not tokens_desconocidos else "léxico",
            "texto": texto,
            "tokens": tokens,
            "errores": errores
        }
    
    def mostrar_resultado(self, resultado: dict):
        """Muestra el resultado del análisis de forma legible"""
        print(f"\n{'='*60}")
        print(f"Texto analizado: '{resultado['texto']}'")
        print(f"{'='*60}")
        
        # Mostrar tokens
        print("\nTokens identificados:")
        for token in resultado['tokens']:
            if token.tipo != TipoToken.FIN:
                print(f"  [{token.tipo.value:12}] -> '{token.valor}'")
        
        # Resultado
        if resultado['valido']:
            print("\n✓ ORACIÓN VÁLIDA - La estructura cumple con la gramática")
        else:
            print(f"\n✗ ORACIÓN INVÁLIDA - Error en fase de análisis {resultado['fase']}")
            print("\nErrores encontrados:")
            for error in resultado['errores']:
                print(f"  • {error}")
        
        print(f"{'='*60}\n")


def main():
    """Función principal con casos de prueba"""
    parser = MiniParser()
    
    print("="*60)
    print("MINI-PARSER PARA LENGUAJE NATURAL LIMITADO")
    print("Parser Descendente Recursivo - Gramática Libre de Contexto")
    print("="*60)
    
    # Casos de prueba válidos
    print("\n" + "="*60)
    print("CASOS DE PRUEBA VÁLIDOS")
    print("="*60)
    
    casos_validos = [
        "el perro come un hueso",
        "la niña lee el libro",
        "un gato grande ve la casa",
        "el niño pequeño quiere un libro rojo",
        "una computadora nueva tiene el carro",
        "los perros buscan las casas",
    ]
    
    for caso in casos_validos:
        resultado = parser.analizar(caso)
        parser.mostrar_resultado(resultado)
    
    # Casos de prueba inválidos
    print("\n" + "="*60)
    print("CASOS DE PRUEBA INVÁLIDOS")
    print("="*60)
    
    casos_invalidos = [
        "el perro grande",  # Falta predicado
        "come el libro",  # Falta sujeto
        "el grande perro come libro",  # Falta artículo en complemento
        "perro el come un libro",  # Orden incorrecto
        "el perro muy grande come el libro",  # Palabra no en vocabulario
        "python es genial",  # Palabras fuera del vocabulario
        "el libro azul hermoso lee la niña",  # Múltiples adjetivos no permitidos
    ]
    
    for caso in casos_invalidos:
        resultado = parser.analizar(caso)
        parser.mostrar_resultado(resultado)


if __name__ == "__main__":
    main()
