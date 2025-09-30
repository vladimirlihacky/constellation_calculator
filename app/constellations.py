from datetime import datetime
import json 

class Constellations(): 
    def __init__(self, data): 
        with open(data, 'r') as f: 
            self.data = json.load(f)

    def generate_seasonal_data(self):
        seasons = {
            'winter': [],
            'spring': [],
            'summer': [], 
            'autumn': []
        }
        
        for constellation in self.constellations:
            seasons[constellation['season']].append({
                'id': constellation['id'],
                'name': constellation['name'],
                'abbreviation': constellation['abbreviation']
            })
        
        return seasons
    
    def find_all(self): 
        return self.data

    def find_visible_at(self, date=datetime.now(), latitude=55):
        current_month = date.month
        visible = []
        
        for constellation in self.data:
            visibility = constellation['visibility']
            
            if (visibility['min_latitude'] <= latitude <= visibility['max_latitude'] and
                current_month in constellation['best_months']):
                
                visible.append(constellation)
        
        return visible
    
    def find_by_id(self, id):
        constellations = [constellation for constellation in self.data if constellation['id'] == id] 
        
        return constellations[0] if constellations else None 