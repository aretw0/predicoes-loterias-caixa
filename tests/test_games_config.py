from core.games.megasena import MegaSena
from core.games.lotofacil import Lotofacil
from core.games.quina import Quina

def test_megasena_config():
    game = MegaSena()
    assert game.range_min == 1
    assert game.range_max == 60
    assert game.draw_count == 6
    assert game.slug == 'megasena'

def test_lotofacil_config():
    game = Lotofacil()
    assert game.range_min == 1
    assert game.range_max == 25
    assert game.draw_count == 15
    assert game.slug == 'lotofacil'

def test_quina_config():
    game = Quina()
    assert game.range_min == 1
    assert game.range_max == 80
    assert game.draw_count == 5
    assert game.slug == 'quina'
