import pandas as pd
import streamlit as st
import requests
from constants.dict_lists_setup import col_letters, row_letters

def get_airtable_headers():
    return {
        "Authorization": f"Bearer {st.secrets['airtable']['token']}",
        "Content-Type": "application/json"
    }

def get_airtable_url():
    base_id = st.secrets["airtable"]["base_id"]
    table = st.secrets["airtable"]["table_name"]
    return f"https://api.airtable.com/v0/{base_id}/{table}"


def get_all_results():
    all_records = []
    url = get_airtable_url()
    params = {}
    while True:
        response = requests.get(url, headers=get_airtable_headers(), params=params)
        result = response.json()
        all_records.extend(result.get("records", []))
        offset = result.get("offset")
        if not offset:
            break
        params["offset"] = offset
    return pd.DataFrame([r["fields"] for r in all_records])

def save_result_airtable(grid, user_answers, duration):
    try:
        stats = {}
        for letter_id in col_letters + row_letters:
            stats[f"Critere {letter_id}"] = grid[f"Criteria {letter_id}"]
        for col_id in col_letters:
            for row_id in row_letters:
                if col_id+row_id in user_answers:
                    stats[f"Arret {col_id+row_id}"] = user_answers[col_id+row_id]
                else : 
                    stats[f"Arret {col_id+row_id}"] = "Non renseigné"
        stats["Temps"] = str(duration)
        
        data = {
            "fields": stats
        }

        response = requests.post(get_airtable_url(), headers=get_airtable_headers(), json=data, timeout=5)
        if response.status_code != 200:
            st.toast("⚠️ Le résultat n'a pas pu être enregistré.", icon="⚠️")
        return response.status_code == 200
    except Exception as e:
        st.toast("⚠️ Le résultat n'a pas pu être enregistré.", icon="⚠️")
        return False