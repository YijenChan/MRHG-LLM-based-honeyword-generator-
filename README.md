## MRHG: Modular and Context-Aware Honeyword Generation Framework
MRHG (Modular and Context-aware Honeyword Generation) is an innovative framework that leverages multiple password generation strategies and adapts dynamically based on recognized password patterns. It uses advanced models, including Large Language Models (LLMs), for intelligent decision-making in generating honeywords, making it robust against various password-guessing attacks.
The system can recognize different password types, such as PII-based, weak, and default passwords, and generate honeywords accordingly. Additionally, it incorporates a Retrieval-Augmented Generation (RAG) strategy to improve password similarity, further enhancing its ability to thwart attackers.Besides, you can access the fine-tuned DeepSeek-7B-base_honeywords (hugging face links: https://huggingface.co/chenyiren/DeepSeek-7B-base_honeywords) to run the framework of multi-prompt routing.

![{1D0CAB75-70EF-4E23-9860-FF21BA3AD339}](https://github.com/user-attachments/assets/570c92ea-4fd8-4706-acdb-d62cb8073852)

## 📌 Key Features
- Dynamic Defense Strategies: MRHG recognizes and adapts to different password patterns including PII-based, weak, and default passwords.
- Intelligent Password Recognition: Uses LLMs to detect whether a password is weak, strong, or linked to PII data.
- Multiple Honeyword Generation Paths: Four key generation paths are supported: Weak Password Generation, Strong Password Generation, Default Password Generation, and PII-based Honeyword Generation.
- RAG Support: Integrates a retrieval-augmented generation mechanism to recommend similar passwords for further protection.
- Interpretability: The generated honeywords are accompanied by explanations in a structured JSON format, which helps in understanding the reasoning behind the generation and allows easy integration with other systems.

## 🧩 Project Structure
```bash
MRHG/
├── README.md                     # Project overview and setup instructions
├── .gitignore                    # Specifies which files to ignore in git
├── requirements.txt              # Project dependencies
├── main.py                       # Main script for honeyword generation
│
├── data/                         # Data directory containing input/output files
│   ├── sample_input.csv          # Example input file containing password data
│   └── hashed_passwords.csv      # CSV file with pre-hashed passwords for RAG support
│
├── src/                          # Core code for honeyword generation, detection, and RAG
│   ├── generators/               # Directory for all honeyword generators
│   │   ├── default_passwords_generator.py
│   │   ├── weak_passwords_generator.py
│   │   ├── strong_passwords_generator.py
│   │   └── pii_based_generator.py
│   │
│   ├── detection/                # Password pattern detection modules
│   │   ├── is_default.py
│   │   ├── is_weak_byllm.py
│   │   └── is_included_pii.py
│   │
│   ├── rag_support/              # RAG module support files
│   │   ├── preprocess_hash_passwords.py
│   │   └── password_recommender.py
│
├── notebooks/                    # Jupyter notebooks for testing and demonstrations
│   └── MRHG_demo.ipynb           # Example demo of MRHG in action
```

## ⚙️ Setup and Installation
### Prerequisites
- **Python 3.11+**
- **OpenAI API Key** (You need to sign up for OpenAI and obtain your API key)

### Step 1: Clone the repository
```bash
git clone https://github.com/yourusername/MRHG.git
cd MRHG
```

### Step 2: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Setup your API key
In `main.py`, replace the placeholder for the API key with your actual OpenAI API key.
```python
client = OpenAI(api_key='your-api-key', base_url="https://apix.ai-gaochao.cn/v1")
```

### Step 4: Running the Main Script
To generate honeywords for a set of passwords, use the following command:
```bash
python main.py
```
This will generate honeywords for the example records provided in `main.py`. You can modify the records or input file to generate honeywords for other passwords.

### Optional: Processing Password Data from CSV

To process a CSV file containing password data and generate honeywords for each record, you can call the `process_csv()` function:

```bash
python main.py --input sample_input.csv --output output.csv
```
This will read passwords from the input CSV file and write the generated honeywords and related information to the output CSV file.

## 📄 Input and Output Formats

### Input Format (CSV)
The input CSV file should contain the following columns:
| Password | Username | Birthday | Name    | Email              |
|----------|----------|----------|---------|--------------------|
| admin    | Nah      | Nah      | Nah     | Nah                |
| David@23 | supercat | 1990-01-01 | Zhangsan | dsan@example.com   |
- Password: The password that you want to generate honeywords for.
- Username, Birthday, Name, Email: Optional fields that may contain personal information, used for pattern detection.

### Output Format (CSV)
The output CSV file will contain the following columns:
| Password | Honeyword_1 | Honeyword_2 | Honeyword_3 | ... | Label  | Reason                                    |
|----------|-------------|-------------|-------------|-----|--------|-------------------------------------------|
| admin    | admin       | guest123    | password123 | ... | DEFAULT | Primary: DEFAULT. Auxiliary: WEAK. Explanation: [details] |
| David@23 | d23test     | david2023   | dav23admin  | ... | PII    | Primary: PII. Auxiliary: STRONG. Explanation: [details] |
- Honeyword_X: The generated honeyword.
- Label: The type of password (e.g., DEFAULT, WEAK, PII).
- Reason: Explanation of why this honeyword was generated, including primary and auxiliary strategies used.

## 🎯 Key Features and Logic
MRHG follows a modular architecture where each password type (PII-based, weak, default, or strong) triggers a different honeyword generation strategy. The logic flows as follows:
1. Identify Password Mode:
   - PII-based: If the record contains personal identifiable information (PII), further checks are made to see if the password incorporates PII.
   - Default: If the password matches common default patterns, it is handled by the Default Password Generator.
   - Weak: If the password is weak, as determined by an external GPT model, it will trigger the Weak Password Generator.
   - Strong: If the password doesn't match the above patterns, it is considered strong and handled by the Strong Password Generator.
     
2. Generate Honeywords:
   - Primary Strategy: The system activates the appropriate primary strategy based on the password mode (PII, Default, Weak, or Strong).
   - Auxiliary Strategies: 80% of the time, the primary strategy is used. 20% of the time, other auxiliary strategies (Weak, Default, Strong) are used alongside the primary one to further confuse the attacker.
     
3. Result:
   - The generated honeywords are returned, including their explanation and the type of strategy used.

![{B8B292E8-7B50-40CE-B0D9-A4CAA2422344}](https://github.com/user-attachments/assets/17223253-5318-4d25-8d05-4a4464786001)

## 🤝 Contributing
We welcome contributions from the community! To contribute:
1. Fork the repository.
2. Clone your fork and create a new branch for your changes.
3. Make your changes and test thoroughly.
4. Submit a pull request with a description of your changes.

## 📝 Final Notes
Feel free to reach out if you have any questions or suggestions for improvements. We encourage collaboration to further enhance MRHG and bring more sophisticated solutions to password security.
