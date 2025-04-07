from weak_passwords_generator import WeakPasswordGenerator
from strong_passwords_generator import StrongPasswordGenerator
from default_passwords_generator import DefaultPasswordHoneywordGenerator
from pii_based_generator import PIIGenerator

from is_default import evaluate_password_strength as evaluate_password_default
from is_weak_byllm import evaluate_password_strength as evaluate_password_weak
from is_included_PII import evaluate_pii_risk as evaluate_password_pii_used

import pandas as pd
import json
import random

class HoneywordsMain:
    def __init__(self, university="XYZ University"):
        self.weak_password_generator = WeakPasswordGenerator(university)
        self.strong_password_generator = StrongPasswordGenerator(university)
        self.default_password_generator = DefaultPasswordHoneywordGenerator(university)
        self.pii_generator = PIIGenerator()

    def is_pii_record(self, record):
        _, username, birthday, name, email = record
        return not (username == 'Nah' and birthday == 'Nah' and name == 'Nah' and email == 'Nah')

    def detect_mode(self, record):
        password, username, birthday, name, email = record
        if self.is_pii_record(record):
            pii_used = evaluate_password_pii_used(record)
            if pii_used and pii_used.get("Tag") == 4:
                return 'PII'
        is_default = evaluate_password_default(password)
        if is_default and is_default.get("Tag") == 1:
            return 'DEFAULT'
        is_weak = evaluate_password_weak(password)
        if is_weak and is_weak.get("Tag") == 2:
            return 'WEAK'
        return 'STRONG'

    def get_aux_strategies(self, primary):
        strategies = ['WEAK', 'STRONG', 'DEFAULT']
        if primary != 'PII':
            strategies.remove('PII')
        if primary in strategies:
            strategies.remove(primary)
        return random.sample(strategies, min(2, len(strategies)))

    def dispatch_generation(self, mode, password, context):
        if mode == 'PII':
            return self.pii_generator.generate(password, *context)
        elif mode == 'DEFAULT':
            return self.default_password_generator.generate(password)
        elif mode == 'WEAK':
            return self.weak_password_generator.generate(password)
        elif mode == 'STRONG':
            return self.strong_password_generator.generate(password)

    def generate_honeywords(self, record):
        password, username, birthday, name, email = record
        context = (username, birthday, name, email)
        mode = self.detect_mode(record)

        primary_result = self.dispatch_generation(mode, password, context)
        honeywords = set(primary_result.get('honeywords', [])) if primary_result else set()
        explanation = f"Primary: {mode}. " + primary_result.get('explanation', '')

        aux_modes = self.get_aux_strategies(mode)
        for aux_mode in aux_modes:
            aux_result = self.dispatch_generation(aux_mode, password, context)
            if aux_result:
                aux_honeywords = aux_result.get('honeywords', [])[:5]
                honeywords.update(aux_honeywords)
                explanation += f" Auxiliary: {aux_mode}. {aux_result.get('explanation', '')}"

        honeywords = list(honeywords)
        if password not in honeywords:
            honeywords.insert(0, password)
        else:
            honeywords.remove(password)
            honeywords.insert(0, password)

        return {
            "label": mode,
            "reason": explanation,
            "honeywords": honeywords[:20]  # limit to 20
        }


def process_csv(input_file, output_file):
    df = pd.read_csv(input_file)
    generator = HoneywordsMain()

    for index, row in df.iterrows():
        password = row['Password']
        username = row.get('Username', 'Nah')
        birthday = row.get('Birthday', 'Nah')
        name = row.get('Name', 'Nah')
        email = row.get('Email', 'Nah')

        record = (password, username, birthday, name, email)
        result = generator.generate_honeywords(record)

        honeywords = result.get("honeywords", [])
        for i, hw in enumerate(honeywords, start=1):
            df.at[index, f'Honeyword_{i}'] = hw

        df.at[index, 'Label'] = result.get("label")
        df.at[index, 'Reason'] = result.get("reason")

        print(f"Processed record {index + 1}: {password} -> {result.get('label')}")

    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"All done. Output saved to {output_file}")


if __name__ == "__main__":
    generator = HoneywordsMain()
    record1 = ("SsanCat3", "supercat", "1995/05/02", "ZhangSan", "hao123@example.com")
    record2 = ("abc123xyz", "Nah", "Nah", "Nah", "Nah")
    record3 = ("DavidLermajr.4894", "Nah", "Nah", "Nah", "Nah")

    for rec in [record1, record2, record3]:
        result = generator.generate_honeywords(rec)
        print(json.dumps(result, indent=4, ensure_ascii=False))