from dataclasses import dataclass

@dataclass
class ConvertibleBondObject:
    ''''''
    vt_symbol:str = ""
    buy_price:float = 0.0
    volume:int = 0.0
    charge_rate:float = 0.001
    
    def __post_init__(self):
        """"""
        self.price:float = self.buy_price 
        self.last_price:float = self.price
        self.position_pct:float = 0.0 
        self.charge:float = self.charge_rate*self.buy_price*self.volume
        self.cost:float = self.buy_price*self.volume*(1+self.charge_rate)
        
        self.pnl_ratio_total:float = self.price*self.volume/self.cost - 1
        self.pnl_total:float = self.price*self.volume - self.cost
        
        self.pnl_ratio_daily:float = self.price/self.last_price - 1
        self.pnl_daily:float = (self.price - self.last_price) * self.volume
            
        self.trade_status:str = "Untraded"
  
    def calculate_daily_result(self,price:float):
        """"""
        self.last_price = self.price
        self.price = price        
        
        self.pnl_total = self.price*self.volume - self.cost
        self.pnl_daily = (self.price - self.last_price) * self.volume
        
        self.pnl_ratio_total = self.price*self.volume/self.cost - 1
        self.pnl_ratio_daily = self.price/self.last_price - 1

class AccountData:
    """Personal Account"""
    accountId:str = "@Alexandre316"
        
    def __init__(self,balance):
        """"""
        self.balance = balance
        self.frozen:float = 0
        self.available:float = self.balance - self.frozen
        
        self.pnl_inday:float = 0.0
        self.pnl_total:float = 0.0
        self.pnl_ratio_total:float = 0.0
            
        self.pnl_ratio_daily:float = 0.0
        self.pnl_daily:float = 0.0
    
        self.in_position_cb:dict = {}
        self.delete_cb:list = []

    def buy(self,vt_symbol:str,buy_price:float,volume:int):
        """"""      
        to_position_cb = ConvertibleBondObject(vt_symbol = vt_symbol,buy_price = buy_price,volume = volume)
        if self.available < to_position_cb.cost:
            return ("Failure Order, Available Not Enough")
        
        self.in_position_cb[to_position_cb.vt_symbol] = to_position_cb
        self.in_position_cb[to_position_cb.vt_symbol].trade_status = "Trading"
        self.frozen += to_position_cb.cost
        self.available -= to_position_cb.cost
        
        return(f"buy {to_position_cb.vt_symbol}|price:{to_position_cb.buy_price}|volume:{to_position_cb.volume}")
    
    def sell(self,vt_symbol:str,sell_price:float,volume:int,status:str = "sell"):
        """"""
        if status == "sell":
            if vt_symbol not in self.in_position_cb.keys():
                return f"You don't have {vt_symbol}"

            to_sell_cb = self.in_position_cb[vt_symbol]
            self.pnl_inday = to_sell_cb.volume * (sell_price - to_sell_cb.price)
            self.frozen += self.pnl_inday
            
            self.in_position_cb[vt_symbol].trade_status = "Sold"
            self.frozen -= (sell_price*to_sell_cb.volume+to_sell_cb.charge) # 
            self.available += sell_price*to_sell_cb.volume # 
            
            to_sell_cb.volume = 0
            self.balance -= to_sell_cb.charge #
            return (f"sell {to_sell_cb.vt_symbol}|price:{sell_price}|volume:{volume}")
        
        # 若是删除卖出，即出现强制赎回
        elif status == "dsell":
            if vt_symbol not in self.in_position_cb.keys():
                return f"You don't have {vt_symbol}"
            
            to_sell_cb = self.in_position_cb[vt_symbol]
            self.pnl_inday = to_sell_cb.volume * (sell_price - to_sell_cb.price)
            self.frozen += self.pnl_inday
            
            self.delete_cb.append(vt_symbol)
            self.in_position_cb[vt_symbol].trade_status = "Sold"
            
            self.frozen -= (sell_price*to_sell_cb.volume+to_sell_cb.charge) #
            self.available += sell_price*to_sell_cb.volume # 
            
            to_sell_cb.volume = 0
            self.balance -= to_sell_cb.charge #
            return (f"sell {to_sell_cb.vt_symbol}|price:{sell_price}|volume:{volume}")
            
        else:
            return "Unsupported Order Status"
        
    def calculate_daily_result(self):
        """callback after cb_object.calculate_daily_result"""
        self.pnl_daily = 0.0
        self.pnl_ratio_daily = 0.0

        for vt_symbol in self.in_position_cb.keys():
            self.pnl_daily += self.in_position_cb[vt_symbol].pnl_daily #
            self.frozen += self.in_position_cb[vt_symbol].pnl_daily #
        
        self.pnl_daily += self.pnl_inday
        self.pnl_ratio_daily = self.pnl_daily/self.balance # 
        self.pnl_total += self.pnl_daily #
        self.pnl_ratio_total = self.pnl_total/self.balance #
        self.balance += self.pnl_daily #
        self.pnl_inday = 0.0
    
    def remove_sold_order(self):
        for vt_symbol in list(self.in_position_cb.keys()):
            if self.in_position_cb[vt_symbol].trade_status == "Sold":
                del self.in_position_cb[vt_symbol]