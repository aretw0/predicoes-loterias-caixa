# Backward compatibility shim
from judge.backtest_ensemble import EnsembleBacktester as EnsembleBacktester
from judge.backtest_standard import Backtester as Backtester
from judge.ensemble import EnsemblePredictor as EnsemblePredictor
from core.base import Lottery as Lottery, Model as Model
from core.games.megasena import MegaSena as MegaSena
from core.games.lotofacil import Lotofacil as Lotofacil
from core.games.quina import Quina as Quina
