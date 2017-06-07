from lightfm.datasets import fetch_movielens
from lightfm import LightFM
import numpy as np

#only select movies with rating more than 4
data = fetch_movielens(min_rating=4.0)

#creating model for recommendation system
model = LightFM(loss='warp')
#train model
model.fit(data['train'], epochs=30, num_threads =2)

def sample_recommendations(model, data, user_ids):
    # number of users and items in our training set
    n_users, n_items = data['train'].shape
                           
    #get movie recommendations for each of the user_ids
    for user_id in user_ids:
        #movies they already like
        known_positives = data['item_labels'][data['train'].tocsr()[user_id].indices]
        
        #movies our model predicts they will like
        scores = model.predict(user_id, np.arange(n_items))
        
        #rank them in order of most liked to least
        top_items = data['item_labels'][np.argsort(-scores)]
        
        #print out the results
        print("User %s" % user_id)
        print("     Known positives:")

        for x in known_positives[:3]:
            print("        %s" % x)

        print("     Recommended:")

        for x in top_items[:3]:
            print("        %s" % x)
            
sample_recommendations(model, data, [3, 25, 450])
        
                                   