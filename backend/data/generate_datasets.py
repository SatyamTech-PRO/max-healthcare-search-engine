"""
Max Healthcare Dataset Generator
Generates 1000 realistic medicines, diagnoses, and investigations
"""

import csv
import os
import random
from faker import Faker

fake = Faker()
random.seed(42)

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────
# MEDICINES (1000)
# ─────────────────────────────────────────────

MEDICINES = [
    # Analgesics / Antipyretics
    ("Paracetamol", "Analgesic/Antipyretic", "Tablet", "500mg"),
    ("Ibuprofen", "NSAID", "Tablet", "400mg"),
    ("Aspirin", "NSAID/Antiplatelet", "Tablet", "75mg"),
    ("Diclofenac", "NSAID", "Tablet", "50mg"),
    ("Naproxen", "NSAID", "Tablet", "500mg"),
    ("Tramadol", "Opioid Analgesic", "Capsule", "50mg"),
    ("Morphine", "Opioid Analgesic", "Injection", "10mg/ml"),
    ("Codeine", "Opioid Analgesic", "Tablet", "30mg"),
    ("Celecoxib", "COX-2 Inhibitor", "Capsule", "200mg"),
    ("Ketorolac", "NSAID", "Injection", "30mg/ml"),
    # Antibiotics
    ("Amoxicillin", "Antibiotic", "Capsule", "500mg"),
    ("Azithromycin", "Antibiotic", "Tablet", "500mg"),
    ("Ciprofloxacin", "Antibiotic", "Tablet", "500mg"),
    ("Metronidazole", "Antibiotic/Antiprotozoal", "Tablet", "400mg"),
    ("Cephalexin", "Antibiotic", "Capsule", "500mg"),
    ("Doxycycline", "Antibiotic", "Capsule", "100mg"),
    ("Clarithromycin", "Antibiotic", "Tablet", "500mg"),
    ("Levofloxacin", "Antibiotic", "Tablet", "500mg"),
    ("Meropenem", "Antibiotic", "Injection", "1g"),
    ("Vancomycin", "Antibiotic", "Injection", "500mg"),
    ("Piperacillin-Tazobactam", "Antibiotic", "Injection", "4.5g"),
    ("Linezolid", "Antibiotic", "Tablet", "600mg"),
    ("Clindamycin", "Antibiotic", "Capsule", "300mg"),
    ("Cotrimoxazole", "Antibiotic", "Tablet", "960mg"),
    ("Nitrofurantoin", "Antibiotic", "Capsule", "100mg"),
    ("Tetracycline", "Antibiotic", "Capsule", "250mg"),
    ("Amoxicillin-Clavulanate", "Antibiotic", "Tablet", "625mg"),
    ("Cefuroxime", "Antibiotic", "Tablet", "500mg"),
    ("Cefixime", "Antibiotic", "Capsule", "200mg"),
    ("Moxifloxacin", "Antibiotic", "Tablet", "400mg"),
    # Antihypertensives
    ("Amlodipine", "Calcium Channel Blocker", "Tablet", "5mg"),
    ("Enalapril", "ACE Inhibitor", "Tablet", "5mg"),
    ("Losartan", "ARB", "Tablet", "50mg"),
    ("Metoprolol", "Beta Blocker", "Tablet", "50mg"),
    ("Atenolol", "Beta Blocker", "Tablet", "50mg"),
    ("Ramipril", "ACE Inhibitor", "Tablet", "5mg"),
    ("Telmisartan", "ARB", "Tablet", "40mg"),
    ("Hydrochlorothiazide", "Diuretic", "Tablet", "25mg"),
    ("Furosemide", "Loop Diuretic", "Tablet", "40mg"),
    ("Spironolactone", "Potassium-Sparing Diuretic", "Tablet", "25mg"),
    ("Bisoprolol", "Beta Blocker", "Tablet", "5mg"),
    ("Carvedilol", "Alpha-Beta Blocker", "Tablet", "6.25mg"),
    ("Nifedipine", "Calcium Channel Blocker", "Tablet", "10mg"),
    ("Verapamil", "Calcium Channel Blocker", "Tablet", "80mg"),
    ("Diltiazem", "Calcium Channel Blocker", "Tablet", "60mg"),
    ("Olmesartan", "ARB", "Tablet", "20mg"),
    ("Valsartan", "ARB", "Tablet", "80mg"),
    ("Candesartan", "ARB", "Tablet", "8mg"),
    ("Perindopril", "ACE Inhibitor", "Tablet", "4mg"),
    ("Lisinopril", "ACE Inhibitor", "Tablet", "10mg"),
    # Antidiabetics
    ("Metformin", "Biguanide", "Tablet", "500mg"),
    ("Glibenclamide", "Sulfonylurea", "Tablet", "5mg"),
    ("Glimepiride", "Sulfonylurea", "Tablet", "2mg"),
    ("Sitagliptin", "DPP-4 Inhibitor", "Tablet", "100mg"),
    ("Empagliflozin", "SGLT2 Inhibitor", "Tablet", "10mg"),
    ("Dapagliflozin", "SGLT2 Inhibitor", "Tablet", "10mg"),
    ("Liraglutide", "GLP-1 Agonist", "Injection", "6mg/ml"),
    ("Insulin Glargine", "Long-Acting Insulin", "Injection", "100U/ml"),
    ("Insulin Regular", "Short-Acting Insulin", "Injection", "100U/ml"),
    ("Insulin Aspart", "Rapid-Acting Insulin", "Injection", "100U/ml"),
    ("Pioglitazone", "Thiazolidinedione", "Tablet", "15mg"),
    ("Vildagliptin", "DPP-4 Inhibitor", "Tablet", "50mg"),
    ("Canagliflozin", "SGLT2 Inhibitor", "Tablet", "100mg"),
    ("Semaglutide", "GLP-1 Agonist", "Injection", "1mg/dose"),
    ("Acarbose", "Alpha-Glucosidase Inhibitor", "Tablet", "50mg"),
    # Statins / Lipid-Lowering
    ("Atorvastatin", "Statin", "Tablet", "10mg"),
    ("Rosuvastatin", "Statin", "Tablet", "10mg"),
    ("Simvastatin", "Statin", "Tablet", "20mg"),
    ("Pravastatin", "Statin", "Tablet", "20mg"),
    ("Fenofibrate", "Fibrate", "Tablet", "145mg"),
    ("Ezetimibe", "Cholesterol Absorption Inhibitor", "Tablet", "10mg"),
    ("Gemfibrozil", "Fibrate", "Tablet", "600mg"),
    # Anticoagulants / Antiplatelets
    ("Warfarin", "Anticoagulant", "Tablet", "5mg"),
    ("Rivaroxaban", "NOAC", "Tablet", "20mg"),
    ("Apixaban", "NOAC", "Tablet", "5mg"),
    ("Dabigatran", "NOAC", "Capsule", "150mg"),
    ("Clopidogrel", "Antiplatelet", "Tablet", "75mg"),
    ("Ticagrelor", "Antiplatelet", "Tablet", "90mg"),
    ("Heparin", "Anticoagulant", "Injection", "5000U/ml"),
    ("Enoxaparin", "LMWH", "Injection", "40mg/0.4ml"),
    # Proton Pump Inhibitors / GI
    ("Omeprazole", "Proton Pump Inhibitor", "Capsule", "20mg"),
    ("Pantoprazole", "Proton Pump Inhibitor", "Tablet", "40mg"),
    ("Rabeprazole", "Proton Pump Inhibitor", "Tablet", "20mg"),
    ("Esomeprazole", "Proton Pump Inhibitor", "Tablet", "40mg"),
    ("Ranitidine", "H2 Blocker", "Tablet", "150mg"),
    ("Domperidone", "Prokinetic", "Tablet", "10mg"),
    ("Ondansetron", "Antiemetic", "Tablet", "4mg"),
    ("Metoclopramide", "Antiemetic", "Tablet", "10mg"),
    ("Loperamide", "Antidiarrheal", "Capsule", "2mg"),
    ("Bisacodyl", "Laxative", "Tablet", "5mg"),
    ("Lactulose", "Laxative", "Syrup", "3.35g/5ml"),
    ("Sucralfate", "Mucosal Protectant", "Tablet", "1g"),
    # Respiratory
    ("Salbutamol", "Bronchodilator", "Inhaler", "100mcg/dose"),
    ("Budesonide", "Corticosteroid Inhaler", "Inhaler", "200mcg/dose"),
    ("Formoterol", "Long-Acting Bronchodilator", "Inhaler", "12mcg/dose"),
    ("Tiotropium", "Anticholinergic Bronchodilator", "Inhaler", "18mcg/dose"),
    ("Montelukast", "Leukotriene Receptor Antagonist", "Tablet", "10mg"),
    ("Theophylline", "Xanthine Bronchodilator", "Tablet", "200mg"),
    ("Ipratropium", "Anticholinergic", "Inhaler", "20mcg/dose"),
    ("Fluticasone", "Corticosteroid", "Inhaler", "250mcg/dose"),
    ("Salmeterol", "Long-Acting Bronchodilator", "Inhaler", "50mcg/dose"),
    ("Dextromethorphan", "Cough Suppressant", "Syrup", "15mg/5ml"),
    # Neurological / Psychiatric
    ("Amlodipine", "Calcium Channel Blocker", "Tablet", "10mg"),
    ("Levetiracetam", "Antiepileptic", "Tablet", "500mg"),
    ("Valproate", "Antiepileptic/Mood Stabilizer", "Tablet", "500mg"),
    ("Carbamazepine", "Antiepileptic", "Tablet", "200mg"),
    ("Phenytoin", "Antiepileptic", "Capsule", "100mg"),
    ("Lamotrigine", "Antiepileptic", "Tablet", "50mg"),
    ("Gabapentin", "Antiepileptic/Neuropathic Pain", "Capsule", "300mg"),
    ("Pregabalin", "Antiepileptic/Neuropathic Pain", "Capsule", "75mg"),
    ("Sertraline", "SSRI Antidepressant", "Tablet", "50mg"),
    ("Fluoxetine", "SSRI Antidepressant", "Capsule", "20mg"),
    ("Escitalopram", "SSRI Antidepressant", "Tablet", "10mg"),
    ("Venlafaxine", "SNRI Antidepressant", "Capsule", "75mg"),
    ("Duloxetine", "SNRI Antidepressant", "Capsule", "60mg"),
    ("Amitriptyline", "TCA Antidepressant", "Tablet", "10mg"),
    ("Olanzapine", "Antipsychotic", "Tablet", "5mg"),
    ("Risperidone", "Antipsychotic", "Tablet", "2mg"),
    ("Clonazepam", "Benzodiazepine", "Tablet", "0.5mg"),
    ("Alprazolam", "Benzodiazepine", "Tablet", "0.25mg"),
    ("Diazepam", "Benzodiazepine", "Tablet", "5mg"),
    ("Zolpidem", "Sedative/Hypnotic", "Tablet", "10mg"),
    ("Donepezil", "Cholinesterase Inhibitor", "Tablet", "5mg"),
    ("Memantine", "NMDA Antagonist", "Tablet", "10mg"),
    ("Levodopa-Carbidopa", "Anti-Parkinson", "Tablet", "250/25mg"),
    # Thyroid
    ("Levothyroxine", "Thyroid Hormone", "Tablet", "50mcg"),
    ("Methimazole", "Antithyroid", "Tablet", "10mg"),
    ("Propylthiouracil", "Antithyroid", "Tablet", "50mg"),
    # Hormones / Endocrine
    ("Prednisolone", "Corticosteroid", "Tablet", "5mg"),
    ("Dexamethasone", "Corticosteroid", "Tablet", "4mg"),
    ("Hydrocortisone", "Corticosteroid", "Injection", "100mg"),
    ("Methylprednisolone", "Corticosteroid", "Injection", "40mg"),
    ("Testosterone", "Androgen", "Injection", "250mg/ml"),
    ("Estradiol", "Estrogen", "Tablet", "2mg"),
    ("Progesterone", "Progestogen", "Capsule", "200mg"),
    # Antimalarials / Antiparasitics
    ("Chloroquine", "Antimalarial", "Tablet", "250mg"),
    ("Hydroxychloroquine", "Antimalarial/DMARD", "Tablet", "200mg"),
    ("Artemether-Lumefantrine", "Antimalarial", "Tablet", "80/480mg"),
    ("Albendazole", "Anthelmintic", "Tablet", "400mg"),
    ("Mebendazole", "Anthelmintic", "Tablet", "100mg"),
    ("Ivermectin", "Antiparasitic", "Tablet", "6mg"),
    # Antivirals
    ("Acyclovir", "Antiviral", "Tablet", "400mg"),
    ("Oseltamivir", "Antiviral", "Capsule", "75mg"),
    ("Tenofovir", "Antiretroviral", "Tablet", "300mg"),
    ("Lamivudine", "Antiretroviral", "Tablet", "150mg"),
    ("Efavirenz", "Antiretroviral", "Tablet", "600mg"),
    ("Sofosbuvir", "Antiviral (HCV)", "Tablet", "400mg"),
    ("Remdesivir", "Antiviral", "Injection", "100mg"),
    # Antifungals
    ("Fluconazole", "Antifungal", "Tablet", "150mg"),
    ("Itraconazole", "Antifungal", "Capsule", "100mg"),
    ("Voriconazole", "Antifungal", "Tablet", "200mg"),
    ("Amphotericin B", "Antifungal", "Injection", "50mg"),
    ("Clotrimazole", "Antifungal", "Cream", "1%"),
    # Vitamins / Supplements
    ("Vitamin D3", "Vitamin", "Tablet", "60000IU"),
    ("Vitamin B12", "Vitamin", "Injection", "1000mcg/ml"),
    ("Folic Acid", "Vitamin", "Tablet", "5mg"),
    ("Iron Sucrose", "Iron Supplement", "Injection", "200mg/10ml"),
    ("Ferrous Sulfate", "Iron Supplement", "Tablet", "325mg"),
    ("Calcium Carbonate", "Calcium Supplement", "Tablet", "500mg"),
    ("Zinc Sulfate", "Mineral", "Tablet", "20mg"),
    ("Vitamin C", "Vitamin", "Tablet", "500mg"),
    ("Vitamin B Complex", "Vitamin", "Tablet", "—"),
    ("Omega-3 Fatty Acids", "Supplement", "Capsule", "1000mg"),
    # Cardiac
    ("Digoxin", "Cardiac Glycoside", "Tablet", "0.25mg"),
    ("Amiodarone", "Antiarrhythmic", "Tablet", "200mg"),
    ("Adenosine", "Antiarrhythmic", "Injection", "6mg/2ml"),
    ("Nitroglycerine", "Nitrate", "Tablet", "0.5mg"),
    ("Isosorbide Mononitrate", "Nitrate", "Tablet", "20mg"),
    ("Ivabradine", "If-Channel Blocker", "Tablet", "5mg"),
    ("Sacubitril-Valsartan", "ARNi", "Tablet", "49/51mg"),
    ("Dobutamine", "Inotrope", "Injection", "250mg/20ml"),
    ("Dopamine", "Vasopressor", "Injection", "200mg/5ml"),
    ("Norepinephrine", "Vasopressor", "Injection", "4mg/4ml"),
    # Immunosuppressants
    ("Azathioprine", "Immunosuppressant", "Tablet", "50mg"),
    ("Methotrexate", "DMARD/Immunosuppressant", "Tablet", "7.5mg"),
    ("Cyclosporine", "Immunosuppressant", "Capsule", "100mg"),
    ("Tacrolimus", "Immunosuppressant", "Capsule", "1mg"),
    ("Mycophenolate Mofetil", "Immunosuppressant", "Tablet", "500mg"),
    # Oncology
    ("Tamoxifen", "Anti-Estrogen", "Tablet", "20mg"),
    ("Imatinib", "Tyrosine Kinase Inhibitor", "Tablet", "400mg"),
    ("Rituximab", "Anti-CD20 Monoclonal Antibody", "Injection", "500mg/50ml"),
    ("Trastuzumab", "HER2 Inhibitor", "Injection", "440mg"),
    ("Bevacizumab", "VEGF Inhibitor", "Injection", "400mg/16ml"),
    # Urology / Nephrology
    ("Tamsulosin", "Alpha Blocker", "Capsule", "0.4mg"),
    ("Finasteride", "5-Alpha Reductase Inhibitor", "Tablet", "5mg"),
    ("Sildenafil", "PDE5 Inhibitor", "Tablet", "50mg"),
    ("Solifenacin", "Anticholinergic", "Tablet", "5mg"),
    ("Desmopressin", "ADH Analogue", "Tablet", "0.1mg"),
    # Ophthalmology
    ("Timolol Eye Drops", "Beta Blocker", "Eye Drops", "0.5%"),
    ("Latanoprost Eye Drops", "Prostaglandin Analogue", "Eye Drops", "0.005%"),
    ("Tobramycin Eye Drops", "Antibiotic", "Eye Drops", "0.3%"),
    ("Sodium Hyaluronate", "Lubricant", "Eye Drops", "0.1%"),
    # Dermatology
    ("Betamethasone", "Topical Corticosteroid", "Cream", "0.1%"),
    ("Tretinoin", "Retinoid", "Cream", "0.025%"),
    ("Adapalene", "Retinoid", "Gel", "0.1%"),
    ("Mupirocin", "Topical Antibiotic", "Ointment", "2%"),
    ("Permethrin", "Antiparasitic", "Cream", "5%"),
    ("Terbinafine", "Antifungal", "Cream", "1%"),
    ("Calcipotriol", "Vitamin D Analogue", "Ointment", "0.005%"),
]

# Manufacturers
MANUFACTURERS = [
    "Sun Pharma", "Cipla", "Dr. Reddy's", "Lupin", "Abbott India",
    "Pfizer India", "Novartis India", "Zydus Cadila", "Alkem Labs",
    "Mankind Pharma", "IPCA Labs", "Torrent Pharma", "Glenmark",
    "Wockhardt", "Emcure Pharma", "Aurobindo Pharma", "Micro Labs",
    "Aristo Pharma", "Elder Pharma", "Sanofi India", "GSK India",
    "Johnson & Johnson", "Himalaya", "Dabur Pharma", "Max Healthcare Pharma"
]

DOSAGE_FORMS = ["Tablet", "Capsule", "Injection", "Syrup", "Inhaler", "Cream",
                "Ointment", "Eye Drops", "Gel", "Patch", "Suppository", "Powder"]

MEDICINE_CATEGORIES = [
    "Analgesic", "Antibiotic", "Antihypertensive", "Antidiabetic", "Statin",
    "Anticoagulant", "Proton Pump Inhibitor", "Bronchodilator", "Antidepressant",
    "Antiepileptic", "Antipsychotic", "Corticosteroid", "Antiviral", "Antifungal",
    "Antimalarial", "Immunosuppressant", "Cardiac", "Vitamin/Supplement",
    "Hormonal", "Dermatological", "Ophthalmic", "Urological", "Oncology", "NSAID"
]


def generate_medicines(count=1000):
    rows = []
    base = MEDICINES.copy()
    # Extend with generated variants
    extra_names = []
    while len(base) + len(extra_names) < count:
        b = random.choice(MEDICINES)
        suffix_options = [
            f"{b[0]} Extended Release", f"{b[0]} Sustained Release",
            f"{b[0]} Dispersible", f"{b[0]} Forte", f"{b[0]} Junior",
            f"{b[0]} Plus", f"{b[0]} IV", f"{b[0]} XR", f"{b[0]} SR",
        ]
        extra_names.append((
            random.choice(suffix_options),
            b[1], b[2],
            random.choice(["10mg", "20mg", "25mg", "50mg", "100mg", "250mg", "500mg", "1g"])
        ))
    all_meds = base + extra_names
    random.shuffle(all_meds)
    seen = set()
    for idx, med in enumerate(all_meds[:count]):
        name = med[0]
        if name in seen:
            name = f"{name} {idx}"
        seen.add(name)
        mfr = random.choice(MANUFACTURERS)
        category = random.choice(MEDICINE_CATEGORIES)
        form = med[2]
        strength = med[3]
        description = (
            f"{name} {strength} {form} is a {med[1].lower()} used in the management of "
            f"various conditions. Manufactured by {mfr}. Each {form.lower()} contains "
            f"{strength} of active ingredient."
        )
        rows.append({
            "id": idx + 1,
            "name": name,
            "generic_name": med[0].split(" Extended")[0].split(" Sustained")[0].split(" Plus")[0],
            "category": category,
            "manufacturer": mfr,
            "dosage_form": form,
            "strength": strength,
            "description": description,
            "drug_class": med[1],
            "prescription_required": random.choice(["Yes", "No", "Yes", "Yes"]),
            "storage": random.choice(["Store below 25°C", "Refrigerate 2-8°C", "Store in dry place", "Store away from light"]),
        })
    return rows


# ─────────────────────────────────────────────
# DIAGNOSES (1000)
# ─────────────────────────────────────────────

DIAGNOSES = [
    # Cardiovascular
    ("Essential Hypertension", "I10", "Cardiology"),
    ("Type 2 Diabetes Mellitus", "E11", "Endocrinology"),
    ("Type 1 Diabetes Mellitus", "E10", "Endocrinology"),
    ("Acute Myocardial Infarction", "I21", "Cardiology"),
    ("Heart Failure", "I50", "Cardiology"),
    ("Atrial Fibrillation", "I48", "Cardiology"),
    ("Ischemic Heart Disease", "I25", "Cardiology"),
    ("Stable Angina Pectoris", "I20", "Cardiology"),
    ("Unstable Angina", "I20.0", "Cardiology"),
    ("Peripheral Arterial Disease", "I73.9", "Cardiology"),
    ("Aortic Stenosis", "I35.0", "Cardiology"),
    ("Mitral Regurgitation", "I34.0", "Cardiology"),
    ("Deep Vein Thrombosis", "I82.4", "Vascular Surgery"),
    ("Pulmonary Embolism", "I26", "Pulmonology"),
    ("Cardiomyopathy", "I42", "Cardiology"),
    ("Pericarditis", "I30", "Cardiology"),
    ("Ventricular Tachycardia", "I47.2", "Cardiology"),
    ("Atrioventricular Block", "I44", "Cardiology"),
    ("Hypertensive Heart Disease", "I11", "Cardiology"),
    # Respiratory
    ("Bronchial Asthma", "J45", "Pulmonology"),
    ("COPD", "J44", "Pulmonology"),
    ("Community-Acquired Pneumonia", "J18", "Pulmonology"),
    ("Pulmonary Tuberculosis", "A15", "Pulmonology"),
    ("Pleural Effusion", "J90", "Pulmonology"),
    ("Pneumothorax", "J93", "Pulmonology"),
    ("Lung Cancer", "C34", "Oncology"),
    ("Interstitial Lung Disease", "J84", "Pulmonology"),
    ("Obstructive Sleep Apnea", "G47.3", "Pulmonology"),
    ("Bronchiectasis", "J47", "Pulmonology"),
    ("Respiratory Failure", "J96", "Critical Care"),
    ("Acute Respiratory Distress Syndrome", "J80", "Critical Care"),
    # Neurological
    ("Ischemic Stroke", "I63", "Neurology"),
    ("Hemorrhagic Stroke", "I61", "Neurology"),
    ("Epilepsy", "G40", "Neurology"),
    ("Migraine", "G43", "Neurology"),
    ("Parkinson's Disease", "G20", "Neurology"),
    ("Alzheimer's Disease", "G30", "Neurology"),
    ("Multiple Sclerosis", "G35", "Neurology"),
    ("Guillain-Barré Syndrome", "G61.0", "Neurology"),
    ("Myasthenia Gravis", "G70.0", "Neurology"),
    ("Meningitis", "G03", "Neurology"),
    ("Encephalitis", "G04", "Neurology"),
    ("Transient Ischemic Attack", "G45.9", "Neurology"),
    ("Bell's Palsy", "G51.0", "Neurology"),
    ("Trigeminal Neuralgia", "G50.0", "Neurology"),
    # Gastrointestinal
    ("Peptic Ulcer Disease", "K27", "Gastroenterology"),
    ("Gastroesophageal Reflux Disease", "K21", "Gastroenterology"),
    ("Irritable Bowel Syndrome", "K58", "Gastroenterology"),
    ("Crohn's Disease", "K50", "Gastroenterology"),
    ("Ulcerative Colitis", "K51", "Gastroenterology"),
    ("Liver Cirrhosis", "K74", "Hepatology"),
    ("Hepatitis B", "B16", "Hepatology"),
    ("Hepatitis C", "B17.1", "Hepatology"),
    ("Non-Alcoholic Fatty Liver Disease", "K76.0", "Hepatology"),
    ("Acute Pancreatitis", "K85", "Gastroenterology"),
    ("Chronic Pancreatitis", "K86.1", "Gastroenterology"),
    ("Colorectal Cancer", "C18", "Oncology"),
    ("Cholecystitis", "K81", "General Surgery"),
    ("Cholelithiasis", "K80", "General Surgery"),
    ("Appendicitis", "K37", "General Surgery"),
    ("Intestinal Obstruction", "K56", "General Surgery"),
    ("Gastrointestinal Bleeding", "K92.2", "Gastroenterology"),
    # Renal
    ("Chronic Kidney Disease", "N18", "Nephrology"),
    ("Acute Kidney Injury", "N17", "Nephrology"),
    ("Nephrotic Syndrome", "N04", "Nephrology"),
    ("Nephritic Syndrome", "N05", "Nephrology"),
    ("Urinary Tract Infection", "N39.0", "Urology"),
    ("Renal Calculi", "N20", "Urology"),
    ("Polycystic Kidney Disease", "Q61.3", "Nephrology"),
    ("Glomerulonephritis", "N05.9", "Nephrology"),
    ("Renal Cell Carcinoma", "C64", "Urology"),
    # Musculoskeletal
    ("Rheumatoid Arthritis", "M06", "Rheumatology"),
    ("Osteoarthritis", "M19", "Rheumatology"),
    ("Systemic Lupus Erythematosus", "M32", "Rheumatology"),
    ("Ankylosing Spondylitis", "M45", "Rheumatology"),
    ("Gout", "M10", "Rheumatology"),
    ("Osteoporosis", "M81", "Rheumatology"),
    ("Fibromyalgia", "M79.7", "Rheumatology"),
    ("Psoriatic Arthritis", "L40.5", "Rheumatology"),
    ("Low Back Pain", "M54.5", "Orthopedics"),
    ("Cervical Spondylosis", "M47.8", "Orthopedics"),
    ("Lumbar Disc Herniation", "M51.1", "Orthopedics"),
    ("Carpal Tunnel Syndrome", "G56.0", "Orthopedics"),
    # Endocrine
    ("Hypothyroidism", "E03", "Endocrinology"),
    ("Hyperthyroidism", "E05", "Endocrinology"),
    ("Cushing's Syndrome", "E24", "Endocrinology"),
    ("Addison's Disease", "E27.1", "Endocrinology"),
    ("Polycystic Ovarian Syndrome", "E28.2", "Gynecology"),
    ("Acromegaly", "E22.0", "Endocrinology"),
    ("Diabetes Insipidus", "E23.2", "Endocrinology"),
    ("Metabolic Syndrome", "E88.81", "Endocrinology"),
    ("Hyperparathyroidism", "E21", "Endocrinology"),
    ("Hypoparathyroidism", "E20", "Endocrinology"),
    # Infectious Diseases
    ("Malaria", "B54", "Infectious Disease"),
    ("Dengue Fever", "A90", "Infectious Disease"),
    ("Typhoid Fever", "A01.0", "Infectious Disease"),
    ("HIV/AIDS", "B20", "Infectious Disease"),
    ("COVID-19", "U07.1", "Infectious Disease"),
    ("Influenza", "J09", "Infectious Disease"),
    ("Sepsis", "A41.9", "Critical Care"),
    ("Cellulitis", "L03", "Dermatology"),
    ("Herpes Zoster", "B02", "Infectious Disease"),
    ("Leptospirosis", "A27", "Infectious Disease"),
    # Hematology
    ("Iron Deficiency Anemia", "D50", "Hematology"),
    ("Vitamin B12 Deficiency Anemia", "D51", "Hematology"),
    ("Sickle Cell Disease", "D57", "Hematology"),
    ("Thalassemia", "D56", "Hematology"),
    ("Aplastic Anemia", "D61", "Hematology"),
    ("Leukemia", "C91", "Hematology/Oncology"),
    ("Lymphoma", "C85", "Hematology/Oncology"),
    ("Multiple Myeloma", "C90.0", "Hematology/Oncology"),
    ("Thrombocytopenia", "D69.6", "Hematology"),
    ("Polycythemia Vera", "D45", "Hematology"),
    # Psychiatric
    ("Major Depressive Disorder", "F32", "Psychiatry"),
    ("Bipolar Disorder", "F31", "Psychiatry"),
    ("Schizophrenia", "F20", "Psychiatry"),
    ("Generalized Anxiety Disorder", "F41.1", "Psychiatry"),
    ("Post-Traumatic Stress Disorder", "F43.1", "Psychiatry"),
    ("Obsessive-Compulsive Disorder", "F42", "Psychiatry"),
    ("Panic Disorder", "F41.0", "Psychiatry"),
    ("Attention Deficit Hyperactivity Disorder", "F90", "Psychiatry"),
    ("Alcohol Use Disorder", "F10", "Psychiatry"),
    # Dermatology
    ("Psoriasis", "L40", "Dermatology"),
    ("Eczema/Atopic Dermatitis", "L20", "Dermatology"),
    ("Acne Vulgaris", "L70.0", "Dermatology"),
    ("Rosacea", "L71", "Dermatology"),
    ("Urticaria", "L50", "Dermatology"),
    ("Melanoma", "C43", "Dermatology/Oncology"),
    ("Seborrheic Dermatitis", "L21", "Dermatology"),
    ("Contact Dermatitis", "L25", "Dermatology"),
    ("Alopecia Areata", "L63", "Dermatology"),
    ("Vitiligo", "L80", "Dermatology"),
    # Gynecology / Obstetrics
    ("Endometriosis", "N80", "Gynecology"),
    ("Uterine Fibroids", "D25", "Gynecology"),
    ("Cervical Cancer", "C53", "Gynecology/Oncology"),
    ("Ovarian Cancer", "C56", "Gynecology/Oncology"),
    ("Breast Cancer", "C50", "Oncology"),
    ("Gestational Diabetes Mellitus", "O24.4", "Obstetrics"),
    ("Pre-eclampsia", "O14", "Obstetrics"),
    ("Ectopic Pregnancy", "O00", "Obstetrics"),
    ("Premature Labor", "O60", "Obstetrics"),
    ("Placenta Previa", "O44", "Obstetrics"),
    # Ophthalmology
    ("Glaucoma", "H40", "Ophthalmology"),
    ("Cataracts", "H26", "Ophthalmology"),
    ("Diabetic Retinopathy", "E11.3", "Ophthalmology"),
    ("Age-Related Macular Degeneration", "H35.3", "Ophthalmology"),
    ("Conjunctivitis", "H10", "Ophthalmology"),
    ("Uveitis", "H20", "Ophthalmology"),
    # ENT
    ("Otitis Media", "H65", "ENT"),
    ("Sinusitis", "J32", "ENT"),
    ("Tonsillitis", "J35.0", "ENT"),
    ("Hearing Loss", "H91", "ENT"),
    ("Vertigo", "H81.3", "ENT"),
    ("Allergic Rhinitis", "J30", "ENT"),
    # Pediatrics
    ("Febrile Seizures", "R56.0", "Pediatrics"),
    ("Acute Gastroenteritis", "A09", "Pediatrics"),
    ("Pneumonia in Children", "J18.9", "Pediatrics"),
    ("Kawasaki Disease", "M30.3", "Pediatrics"),
    ("Neonatal Jaundice", "P59", "Neonatology"),
    ("Autism Spectrum Disorder", "F84", "Pediatrics"),
]

SPECIALTIES = [
    "Cardiology", "Pulmonology", "Neurology", "Gastroenterology", "Hepatology",
    "Nephrology", "Endocrinology", "Rheumatology", "Hematology", "Oncology",
    "Psychiatry", "Dermatology", "Gynecology", "Obstetrics", "Urology",
    "Orthopedics", "Ophthalmology", "ENT", "Pediatrics", "Infectious Disease",
    "Critical Care", "General Surgery", "Neonatology", "Vascular Surgery"
]


def generate_diagnoses(count=1000):
    rows = []
    base = DIAGNOSES.copy()
    extra = []
    modifiers = ["Acute", "Chronic", "Severe", "Mild", "Moderate", "Recurrent",
                 "Primary", "Secondary", "Early-Onset", "Late-Onset", "Idiopathic",
                 "Congenital", "Post-Operative", "Drug-Induced", "Autoimmune"]
    while len(base) + len(extra) < count:
        b = random.choice(DIAGNOSES)
        mod = random.choice(modifiers)
        extra.append((f"{mod} {b[0]}", b[1] + ".X", b[2]))
    all_diag = (base + extra)[:count]
    random.shuffle(all_diag)
    seen = set()
    for idx, d in enumerate(all_diag):
        name = d[0]
        if name in seen:
            name = f"{name} Type {idx % 4 + 1}"
        seen.add(name)
        spec = d[2] if d[2] in SPECIALTIES else random.choice(SPECIALTIES)
        description = (
            f"{name} (ICD-10: {d[1]}) is a clinical diagnosis managed under "
            f"{spec}. Characterized by a range of symptoms requiring thorough "
            f"clinical evaluation, diagnostic workup, and individualized treatment planning."
        )
        rows.append({
            "id": idx + 1,
            "name": name,
            "icd_code": d[1],
            "specialty": spec,
            "description": description,
            "severity": random.choice(["Mild", "Moderate", "Severe", "Variable"]),
            "chronic": random.choice(["Yes", "No", "Variable"]),
            "treatment_available": random.choice(["Yes", "Supportive", "Curative"]),
            "prevalence": random.choice(["Common", "Uncommon", "Rare", "Very Common"]),
        })
    return rows


# ─────────────────────────────────────────────
# INVESTIGATIONS (1000)
# ─────────────────────────────────────────────

INVESTIGATIONS = [
    # Hematology
    ("Complete Blood Count", "Hematology", "Blood (EDTA)", "Routine blood test measuring RBC, WBC, platelets, hemoglobin, and hematocrit"),
    ("Hemoglobin Estimation", "Hematology", "Blood (EDTA)", "Measures hemoglobin concentration in blood"),
    ("Peripheral Blood Smear", "Hematology", "Blood (EDTA)", "Microscopic examination of blood cells for morphology"),
    ("ESR (Erythrocyte Sedimentation Rate)", "Hematology", "Blood (EDTA)", "Measures rate of red blood cell sedimentation"),
    ("Reticulocyte Count", "Hematology", "Blood (EDTA)", "Counts immature red blood cells to assess bone marrow activity"),
    ("Platelet Count", "Hematology", "Blood (EDTA)", "Quantifies platelets for bleeding/clotting assessment"),
    ("Coagulation Profile (PT/INR/aPTT)", "Hematology", "Blood (Citrate)", "Assesses clotting factor function and anticoagulation therapy"),
    ("D-Dimer", "Hematology", "Blood (Citrate)", "Fibrin degradation product indicating thrombosis or DIC"),
    ("Bone Marrow Biopsy", "Hematology", "Bone Marrow", "Histological examination of bone marrow for hematologic disorders"),
    ("Fibrinogen Level", "Hematology", "Blood (Citrate)", "Measures fibrinogen for coagulation assessment"),
    # Biochemistry
    ("Fasting Blood Glucose", "Biochemistry", "Blood (Fluoride Oxalate)", "Measures blood sugar after 8-hour fast"),
    ("Post-Prandial Blood Glucose", "Biochemistry", "Blood (Fluoride Oxalate)", "Measures blood sugar 2 hours after meal"),
    ("HbA1c (Glycated Hemoglobin)", "Biochemistry", "Blood (EDTA)", "3-month average blood glucose control marker"),
    ("Serum Creatinine", "Biochemistry", "Blood (Plain)", "Kidney function marker measuring creatinine clearance"),
    ("Blood Urea Nitrogen", "Biochemistry", "Blood (Plain)", "Assesses kidney function and protein catabolism"),
    ("Serum Uric Acid", "Biochemistry", "Blood (Plain)", "Measures uric acid for gout and kidney stone assessment"),
    ("Lipid Profile", "Biochemistry", "Blood (Plain)", "Measures cholesterol, LDL, HDL, triglycerides"),
    ("Liver Function Tests", "Biochemistry", "Blood (Plain)", "Panel measuring bilirubin, albumin, liver enzymes"),
    ("Serum Electrolytes (Na/K/Cl)", "Biochemistry", "Blood (Plain)", "Measures sodium, potassium, chloride levels"),
    ("Serum Calcium", "Biochemistry", "Blood (Plain)", "Measures total calcium for bone and parathyroid assessment"),
    ("Serum Phosphorus", "Biochemistry", "Blood (Plain)", "Measures phosphate for bone mineral metabolism"),
    ("Serum Albumin", "Biochemistry", "Blood (Plain)", "Protein marker for nutritional status and liver function"),
    ("Serum Bilirubin (Total/Direct)", "Biochemistry", "Blood (Plain)", "Measures bilirubin for jaundice evaluation"),
    ("SGOT/AST", "Biochemistry", "Blood (Plain)", "Liver and muscle enzyme marker"),
    ("SGPT/ALT", "Biochemistry", "Blood (Plain)", "Liver-specific enzyme for hepatocellular damage"),
    ("Alkaline Phosphatase", "Biochemistry", "Blood (Plain)", "Liver/bone enzyme elevated in cholestasis"),
    ("GGT (Gamma-GT)", "Biochemistry", "Blood (Plain)", "Sensitive liver enzyme for alcohol and biliary disease"),
    ("Serum Amylase", "Biochemistry", "Blood (Plain)", "Pancreatic enzyme elevated in acute pancreatitis"),
    ("Serum Lipase", "Biochemistry", "Blood (Plain)", "More specific pancreatic enzyme than amylase"),
    ("Serum LDH", "Biochemistry", "Blood (Plain)", "Tissue damage marker used in hemolysis and cancer"),
    ("CPK/CK (Creatine Kinase)", "Biochemistry", "Blood (Plain)", "Muscle/heart enzyme marker for MI and myopathy"),
    ("Troponin I/T", "Biochemistry", "Blood (Plain)", "High-sensitivity cardiac marker for acute MI"),
    ("BNP/NT-proBNP", "Biochemistry", "Blood (Plain)", "Heart failure biomarker for ventricular stress"),
    ("CRP (C-Reactive Protein)", "Biochemistry", "Blood (Plain)", "Acute phase inflammatory marker"),
    ("Procalcitonin", "Biochemistry", "Blood (Plain)", "Sepsis biomarker distinguishing bacterial from viral"),
    ("TSH (Thyroid Stimulating Hormone)", "Biochemistry", "Blood (Plain)", "Primary screening test for thyroid disorders"),
    ("Free T3 and T4", "Biochemistry", "Blood (Plain)", "Thyroid hormone levels for hypo/hyperthyroidism"),
    ("Serum Ferritin", "Biochemistry", "Blood (Plain)", "Iron storage marker for anemia and iron overload"),
    ("Serum Iron and TIBC", "Biochemistry", "Blood (Plain)", "Iron metabolism panel for anemia classification"),
    ("Vitamin D (25-OH)", "Biochemistry", "Blood (Plain)", "Measures vitamin D status"),
    ("Vitamin B12", "Biochemistry", "Blood (Plain)", "Measures cobalamin for neuropathy and anemia"),
    ("Folate Level", "Biochemistry", "Blood (Plain)", "Measures folic acid for megaloblastic anemia"),
    ("Serum Cortisol", "Biochemistry", "Blood (Plain)", "Adrenal function marker for Cushing/Addison"),
    ("Insulin Level", "Biochemistry", "Blood (Plain)", "Measures insulin for insulin resistance assessment"),
    ("C-Peptide", "Biochemistry", "Blood (Plain)", "Distinguishes Type 1 from Type 2 diabetes"),
    ("PSA (Prostate Specific Antigen)", "Biochemistry", "Blood (Plain)", "Prostate cancer screening marker"),
    ("CEA (Carcinoembryonic Antigen)", "Biochemistry", "Blood (Plain)", "Tumor marker for colorectal cancer monitoring"),
    ("AFP (Alpha-Fetoprotein)", "Biochemistry", "Blood (Plain)", "Liver cancer and prenatal screening marker"),
    ("CA-125", "Biochemistry", "Blood (Plain)", "Ovarian cancer biomarker"),
    ("CA 19-9", "Biochemistry", "Blood (Plain)", "Pancreatic cancer monitoring marker"),
    ("HCG (Beta)", "Biochemistry", "Blood/Urine", "Pregnancy test and testicular/trophoblastic tumor marker"),
    # Microbiology
    ("Blood Culture and Sensitivity", "Microbiology", "Blood", "Detects bacterial/fungal bloodstream infections"),
    ("Urine Culture and Sensitivity", "Microbiology", "Urine (Mid-Stream)", "Identifies uropathogens and antibiotic sensitivity"),
    ("Sputum Culture", "Microbiology", "Sputum", "Identifies respiratory pathogens"),
    ("Sputum for AFB (Acid-Fast Bacilli)", "Microbiology", "Sputum", "Screens for Mycobacterium tuberculosis"),
    ("Stool Culture", "Microbiology", "Stool", "Identifies enteric pathogens in GI infections"),
    ("Throat Swab Culture", "Microbiology", "Throat Swab", "Identifies Streptococcus and other pharyngeal pathogens"),
    ("CSF Culture and Analysis", "Microbiology", "CSF", "Evaluates meningitis and CNS infections"),
    ("Wound Swab Culture", "Microbiology", "Wound Swab", "Identifies pathogens in infected wounds"),
    ("MRSA Screening", "Microbiology", "Nasal/Skin Swab", "Screens for methicillin-resistant Staphylococcus aureus"),
    ("Malarial Antigen (RDT)", "Microbiology", "Blood", "Rapid detection of Plasmodium species antigens"),
    ("Dengue NS1 Antigen", "Microbiology", "Blood (Plain)", "Early dengue fever detection antigen"),
    ("Dengue IgM/IgG Antibodies", "Microbiology", "Blood (Plain)", "Serological diagnosis of dengue fever"),
    ("Typhoid Widal Test", "Microbiology", "Blood (Plain)", "Antibody test for Salmonella typhi"),
    ("Hepatitis B Surface Antigen (HBsAg)", "Microbiology", "Blood (Plain)", "Screens for active hepatitis B infection"),
    ("Anti-HCV Antibody", "Microbiology", "Blood (Plain)", "Screens for hepatitis C infection"),
    ("HIV ELISA (1&2)", "Microbiology", "Blood (Plain)", "Screening test for HIV infection"),
    ("COVID-19 RT-PCR", "Microbiology", "Nasopharyngeal Swab", "Molecular detection of SARS-CoV-2"),
    ("COVID-19 Antigen Test", "Microbiology", "Nasopharyngeal Swab", "Rapid antigen detection for COVID-19"),
    ("Venereal Disease Research Lab (VDRL)", "Microbiology", "Blood (Plain)", "Syphilis screening test"),
    ("Treponema Pallidum Antibody (TPHA)", "Microbiology", "Blood (Plain)", "Confirmatory test for syphilis"),
    # Immunology
    ("ANA (Antinuclear Antibody)", "Immunology", "Blood (Plain)", "Screening test for autoimmune disorders"),
    ("Anti-dsDNA Antibody", "Immunology", "Blood (Plain)", "Specific for Systemic Lupus Erythematosus"),
    ("Rheumatoid Factor (RF)", "Immunology", "Blood (Plain)", "Antibody marker for rheumatoid arthritis"),
    ("Anti-CCP Antibody", "Immunology", "Blood (Plain)", "Highly specific marker for rheumatoid arthritis"),
    ("Complement (C3/C4)", "Immunology", "Blood (Plain)", "Complement system evaluation for autoimmune disease"),
    ("ANCA (Anti-Neutrophil Cytoplasmic Antibody)", "Immunology", "Blood (Plain)", "Vasculitis screening marker"),
    ("Immunoglobulins (IgG/IgM/IgA)", "Immunology", "Blood (Plain)", "Measures antibody levels for immunodeficiency"),
    ("Allergy Panel (IgE)", "Immunology", "Blood (Plain)", "Identifies specific allergen sensitization"),
    ("CD4 Count (T-Cell)", "Immunology", "Blood (EDTA)", "HIV disease progression monitoring"),
    ("HLA-B27", "Immunology", "Blood (EDTA)", "Genetic marker for ankylosing spondylitis"),
    # Radiology
    ("Chest X-Ray (PA View)", "Radiology", "—", "Imaging of lungs, heart, and mediastinum"),
    ("X-Ray Abdomen (Erect)", "Radiology", "—", "Evaluates bowel obstruction, perforation"),
    ("X-Ray Spine (Cervical/Lumbar)", "Radiology", "—", "Evaluates vertebral alignment and disc spaces"),
    ("X-Ray Knee/Hip/Shoulder", "Radiology", "—", "Joint space evaluation for arthritis and fractures"),
    ("Ultrasound Abdomen and Pelvis", "Radiology", "—", "Soft tissue imaging of abdominal organs"),
    ("Ultrasound Thyroid", "Radiology", "—", "Evaluates thyroid gland morphology and nodules"),
    ("Ultrasound Obstetric", "Radiology", "—", "Fetal growth, placenta, amniotic fluid assessment"),
    ("CT Scan Head (Plain/Contrast)", "Radiology", "—", "Brain imaging for stroke, tumor, trauma"),
    ("CT Scan Chest (HRCT)", "Radiology", "—", "High-resolution lung parenchyma imaging"),
    ("CT Scan Abdomen and Pelvis", "Radiology", "—", "Detailed abdominal organ and vascular imaging"),
    ("CT Pulmonary Angiography (CTPA)", "Radiology", "—", "Gold standard for pulmonary embolism diagnosis"),
    ("MRI Brain", "Radiology", "—", "Detailed CNS imaging for tumors, MS, stroke"),
    ("MRI Spine", "Radiology", "—", "Spinal cord and disc herniation assessment"),
    ("MRI Knee", "Radiology", "—", "Ligament, meniscus, and cartilage evaluation"),
    ("PET Scan", "Radiology", "—", "Metabolic imaging for cancer staging and response"),
    ("Bone Scan (DEXA)", "Radiology", "—", "Bone mineral density for osteoporosis diagnosis"),
    ("Echocardiography (Echo)", "Cardiology", "—", "Cardiac structure and function assessment"),
    ("Doppler Ultrasound (Arterial/Venous)", "Radiology", "—", "Blood flow assessment in vessels"),
    ("Mammography", "Radiology", "—", "Breast tissue screening for cancer"),
    ("HSG (Hysterosalpingography)", "Radiology", "—", "Uterine and fallopian tube patency assessment"),
    # Cardiology
    ("Electrocardiogram (ECG/EKG)", "Cardiology", "—", "12-lead cardiac electrical activity recording"),
    ("Holter Monitor (24-hour ECG)", "Cardiology", "—", "Continuous cardiac rhythm monitoring"),
    ("Treadmill Test (TMT/Exercise Stress Test)", "Cardiology", "—", "Exercise-induced cardiac ischemia assessment"),
    ("Coronary Angiography (CAG)", "Cardiology", "Blood (Femoral/Radial)", "Invasive visualization of coronary arteries"),
    ("Cardiac Catheterization", "Cardiology", "Blood", "Hemodynamic assessment of cardiac chambers"),
    ("Ambulatory Blood Pressure Monitoring", "Cardiology", "—", "24-hour blood pressure pattern assessment"),
    # Endoscopy
    ("Upper GI Endoscopy (OGD Scope)", "Endoscopy", "—", "Visualization of esophagus, stomach, duodenum"),
    ("Colonoscopy", "Endoscopy", "—", "Colon and rectum visualization for polyps/cancer"),
    ("ERCP", "Endoscopy", "—", "Biliary and pancreatic duct evaluation"),
    ("Bronchoscopy", "Endoscopy", "—", "Airway visualization and bronchial biopsy"),
    ("Cystoscopy", "Endoscopy", "—", "Bladder and urethra direct visualization"),
    ("Sigmoidoscopy", "Endoscopy", "—", "Sigmoid colon and rectum examination"),
    # Urinalysis
    ("Urine Routine and Microscopy", "Biochemistry", "Urine (Mid-Stream)", "Screens for UTI, renal disease, metabolic disorders"),
    ("24-Hour Urine Protein", "Biochemistry", "Urine (24h)", "Quantifies proteinuria for renal disease staging"),
    ("Urine Microalbumin", "Biochemistry", "Urine (Spot)", "Early diabetic nephropathy detection"),
    ("Urine Bence-Jones Protein", "Biochemistry", "Urine (24h)", "Multiple myeloma screening marker"),
    ("Urine Ketone Bodies", "Biochemistry", "Urine", "Diabetic ketoacidosis screening"),
    # Pulmonology
    ("Spirometry (PFT)", "Pulmonology", "Breath", "Lung function assessment for asthma and COPD"),
    ("ABG (Arterial Blood Gas)", "Pulmonology", "Arterial Blood", "Blood pH, oxygenation, and CO2 assessment"),
    ("Pulse Oximetry", "Pulmonology", "—", "Non-invasive SpO2 monitoring"),
    ("Peak Expiratory Flow Rate (PEFR)", "Pulmonology", "Breath", "Asthma monitoring tool"),
    ("FeNO (Fractional Exhaled Nitric Oxide)", "Pulmonology", "Breath", "Airway eosinophilic inflammation marker"),
    # Pathology
    ("Fine Needle Aspiration Cytology (FNAC)", "Pathology", "Tissue Aspirate", "Cytological examination of nodules/masses"),
    ("Core Needle Biopsy", "Pathology", "Tissue Core", "Histological examination of solid tumors"),
    ("Lymph Node Biopsy", "Pathology", "Tissue", "Diagnosis of lymphoma and metastatic disease"),
    ("Skin Biopsy", "Pathology", "Skin", "Histological skin lesion diagnosis"),
    ("Liver Biopsy", "Pathology", "Liver Tissue", "Hepatic fibrosis staging and diagnosis"),
    ("Renal Biopsy", "Pathology", "Kidney Tissue", "Glomerular disease classification"),
    ("Pap Smear", "Pathology", "Cervical Cells", "Cervical cancer screening"),
    ("Endometrial Biopsy", "Pathology", "Endometrial Tissue", "Uterine pathology assessment"),
    # Neurology
    ("EEG (Electroencephalogram)", "Neurology", "—", "Brain electrical activity for seizure diagnosis"),
    ("Nerve Conduction Velocity (NCV)", "Neurology", "—", "Peripheral nerve function assessment"),
    ("EMG (Electromyography)", "Neurology", "—", "Muscle electrical activity assessment"),
    ("Lumbar Puncture (CSF Analysis)", "Neurology", "CSF", "CNS infection and demyelination diagnosis"),
    ("Visual Evoked Potential (VEP)", "Neurology", "—", "Optic nerve function assessment"),
    ("BAER (Brainstem Auditory Evoked Response)", "Neurology", "—", "Brainstem and auditory pathway assessment"),
    # Ophthalmology
    ("Intraocular Pressure (Tonometry)", "Ophthalmology", "—", "Glaucoma screening and monitoring"),
    ("Visual Field Test (Perimetry)", "Ophthalmology", "—", "Peripheral vision assessment"),
    ("Fundus Photography", "Ophthalmology", "—", "Retina and optic disc imaging"),
    ("OCT (Optical Coherence Tomography)", "Ophthalmology", "—", "Retinal layer cross-sectional imaging"),
    ("Slit Lamp Examination", "Ophthalmology", "—", "Anterior segment eye examination"),
    # Genetics / Molecular
    ("Chromosomal Karyotyping", "Genetics", "Blood (Heparin)", "Chromosomal abnormality detection"),
    ("FISH (Fluorescence In-Situ Hybridization)", "Genetics", "Tissue/Blood", "Specific chromosomal deletion/translocation detection"),
    ("BCR-ABL PCR", "Hematology/Molecular", "Blood", "CML monitoring and diagnosis"),
    ("JAK2 Mutation", "Hematology/Molecular", "Blood (EDTA)", "Polycythemia vera and MPN diagnosis"),
    ("BRCA1/BRCA2 Gene Testing", "Genetics", "Blood (EDTA)", "Hereditary breast/ovarian cancer risk assessment"),
    ("Thyroglobulin Antibody", "Biochemistry", "Blood (Plain)", "Thyroid autoimmunity and cancer monitoring"),
    ("Anti-TPO Antibody", "Immunology", "Blood (Plain)", "Hashimoto's thyroiditis diagnosis"),
    ("HLA Typing", "Genetics", "Blood (EDTA)", "Organ transplant matching and disease association"),
    # Stool / Special
    ("Stool for Occult Blood (FOB)", "Biochemistry", "Stool", "Colorectal cancer and GI bleeding screening"),
    ("Stool for Ova and Parasite", "Microbiology", "Stool", "Intestinal parasitic infection detection"),
    ("H. Pylori Urea Breath Test", "Gastroenterology", "Breath", "Non-invasive H. pylori detection"),
    ("H. Pylori Antigen (Stool)", "Microbiology", "Stool", "H. pylori infection detection in stool"),
    ("Rapid Plasma Reagin (RPR)", "Microbiology", "Blood (Plain)", "Syphilis activity monitoring test"),
]

DEPARTMENTS = [
    "Hematology", "Biochemistry", "Microbiology", "Immunology", "Radiology",
    "Cardiology", "Pathology", "Neurology", "Pulmonology", "Endoscopy",
    "Ophthalmology", "Genetics", "Gastroenterology", "Gynecology", "Urology"
]

SAMPLE_TYPES = [
    "Blood (EDTA)", "Blood (Plain)", "Blood (Citrate)", "Blood (Fluoride Oxalate)",
    "Urine (Mid-Stream)", "Urine (24h)", "Urine (Spot)", "Stool",
    "Sputum", "CSF", "Tissue", "Swab", "Arterial Blood", "Breath", "—"
]


def generate_investigations(count=1000):
    rows = []
    base = INVESTIGATIONS.copy()
    extra = []
    modifiers = ["Quantitative", "Qualitative", "Rapid", "Confirmatory", "Serial",
                 "Extended", "High-Sensitivity", "Point-of-Care", "Automated",
                 "Conventional", "Fluorescent", "Immunoassay", "Digital", "Advanced"]
    while len(base) + len(extra) < count:
        b = random.choice(INVESTIGATIONS)
        mod = random.choice(modifiers)
        extra.append((f"{mod} {b[0]}", b[1], b[2], f"{mod.lower()} method of {b[3]}"))
    all_inv = (base + extra)[:count]
    random.shuffle(all_inv)
    seen = set()
    for idx, inv in enumerate(all_inv):
        name = inv[0]
        if name in seen:
            name = f"{name} ({idx})"
        seen.add(name)
        dept = inv[1] if inv[1] in DEPARTMENTS else random.choice(DEPARTMENTS)
        sample = inv[2] if inv[2] in SAMPLE_TYPES else random.choice(SAMPLE_TYPES)
        rows.append({
            "id": idx + 1,
            "name": name,
            "department": dept,
            "sample_type": sample,
            "description": inv[3],
            "turnaround_time": random.choice(["1 hour", "2 hours", "4 hours", "6 hours", "Same day", "24 hours", "48 hours", "72 hours"]),
            "fasting_required": random.choice(["Yes", "No", "8 hours", "12 hours"]),
            "normal_range": random.choice(["See report", "Lab-specific", "Age/sex dependent", "Standardized"]),
            "cost_category": random.choice(["Basic", "Standard", "Specialized", "Advanced"]),
        })
    return rows


def write_csv(filename, rows, fieldnames):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"✅ Written {len(rows)} rows → {filepath}")


if __name__ == "__main__":
    print("🏥 Generating Max Healthcare Datasets...")

    medicines = generate_medicines(1000)
    write_csv("medicines.csv", medicines, medicines[0].keys())

    diagnoses = generate_diagnoses(1000)
    write_csv("diagnoses.csv", diagnoses, diagnoses[0].keys())

    investigations = generate_investigations(1000)
    write_csv("investigations.csv", investigations, investigations[0].keys())

    print("\n✅ All datasets generated successfully!")
    print(f"   Medicines: {len(medicines)}")
    print(f"   Diagnoses: {len(diagnoses)}")
    print(f"   Investigations: {len(investigations)}")
