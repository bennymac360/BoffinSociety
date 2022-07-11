#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 21:54:55 2022

@author: ben
"""

import http.client
import json    # or `import simplejson as json` if on Python < 2.6
import os
import http.client
from theblockchainapi import SolanaAPIResource
import requests

RESOURCE = SolanaAPIResource(        
    api_key_id = "veLcHNd2YcWYkgZ",
    api_secret_key = "9yVLAH4NbYglKSi"
    
)

snipe_price = 0.14 #solana
buyerPubKey = 00000000000000000000000000000


#Connect to ME and get data on last 20 listed NFTs
conn = http.client.HTTPSConnection("api-mainnet.magiceden.dev")
payload = ''
headers = {}
conn.request("GET", "/v2/collections/bofficedoor/listings?offset=0&limit=20", payload, headers)
res = conn.getresponse()
data = res.read()
data_list = json.loads(data)    # obj now contains a dict of the data


#Initialise dict
listed_mint = []
listed_price = []
listed_seller = []
listed_auction = []
listed_ata = []
listed_pda = []
listed_refer = []

# Check for conditions and append 
for obj in data_list:
    # Search the key value using 'in' operator
    if float(obj["price"]) < snipe_price:
            listed_mint.append(str(obj["tokenMint"]))
            listed_price.append(obj["price"])
            listed_seller.append(obj["seller"])
            listed_auction.append(obj["auctionHouse"])
            listed_pda.append(obj["pdaAddress"])
            listed_refer.append(obj["sellerReferral"])



            ata = RESOURCE.get_associated_token_account_address(
                
                    mint_address = str(obj["tokenMint"]),
                public_key = str(obj["seller"])
            )
            print(ata)
            listed_ata.append(ata)


for i in range(len(listed_mint)):
    
    sellerPubKey = listed_seller[i]
    auctionHouseAddress = listed_auction[i]
    mintAccAddress = listed_mint[i]
    tokenAta = listed_ata[i]
    price = listed_price[i]

url = "http://api-devnet.magiceden.dev/v2/instructions/buy_now?buyer="+str(buyerPubKey)+"&seller="+str(sellerPubKey)+"&auctionHouseAddress="+str(auctionHouseAddress)+"&tokenMint="+str(mintAccAddress)+"&tokenATA="+str(tokenAta)+"&price="+str(price)+"&buyerReferral=&sellerReferral=&buyerExpiry=&sellerExpiry=0"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)


