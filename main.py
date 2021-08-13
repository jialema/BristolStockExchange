from exchange import Exchange
from market_maker import MarketMaker
from liquidity_consumer import LiquidityConsumer
from momentum_trader import MomentumTrader
from mean_reversion_trader import MeanReversionTrader
import util
import time
import random
from pprint import pprint

def main():
	exchange = Exchange()
	print(exchange)

	market_maker = MarketMaker()
	print(market_maker)

	liquidity_consumer = LiquidityConsumer()
	print(liquidity_consumer)

	momentum_trader = MomentumTrader()
	print(momentum_trader)

	mean_reversion_trader = MeanReversionTrader()
	print(mean_reversion_trader)

	traders = dict()
	traders[market_maker.trader_id] = market_maker
	traders[liquidity_consumer.trader_id] = liquidity_consumer
	traders[momentum_trader.trader_id] = momentum_trader
	traders[mean_reversion_trader.trader_id] = mean_reversion_trader

	"""
	a simulated day is divided into 300,000 periods, 
	# approximately the number of 10ths of a second in an 8.5h trading day
	"""
	cur_time = 0
	total_time = 300000
	while cur_time < total_time:
		# market maker
		ask_order, bid_order = market_maker.work(exchange, cur_time)
		if ask_order is not None:
			# cancel any existing orders from market maker
			exchange.del_any_existing_orders_by_trader(market_maker.trader_id)
			# sent ask order to exchange
			trades = exchange.make_match(cur_time, ask_order, False)
			util.process_trades(trades, traders, ask_order, cur_time)
			# sent bid order to exchange
			trades = exchange.process_order(cur_time, bid_order, False)
			util.process_trades(trades, traders, bid_order, cur_time)

		# liquidity consumer
		if cur_time == 0:
			# initialize internal parameters at start of day
			liquidity_consumer.make_decision()
		order = liquidity_consumer.work(exchange, cur_time)
		if order is not None:
			trades = exchange.process_order(cur_time, order, False)
			util.process_trades(trades, traders, ask_order, cur_time)

		# momentum trader
		order = momentum_trader.work(exchange, cur_time)
		if order is not None:
			trades = exchange.process_order(cur_time, order, False)
			util.process_trades(trades, traders, order, cur_time)

		# mean reversion trader
		order = mean_reversion_trader.work(exchange, cur_time)
		if order is not None:
			trades = exchange.process_order(cur_time, order, False)
			util.process_trades(trades, traders, order, cur_time)

		# noise trader
		

		cur_time += 1
	pprint(exchange.tape)


if __name__ == "__main__":
	main()
