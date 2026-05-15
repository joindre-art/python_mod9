#!/usr/bin/env bash
# Cosmic Data - Setup automatique
# Cree les 3 venvs, installe pydantic dans chacun, et genere les donnees de test.

set -e  # Arrete le script a la moindre erreur

echo "======================================"
echo "  Cosmic Data - Setup"
echo "======================================"
echo ""

# 1. Creation des venvs et installation de pydantic
for ex in ex0 ex1 ex2; do
    echo ">>> Setup $ex/"
    if [ ! -d "$ex/venv" ]; then
        python3 -m venv "$ex/venv"
        echo "    venv cree"
    else
        echo "    venv deja existant"
    fi
    "$ex/venv/bin/pip" install --quiet --upgrade pip
    "$ex/venv/bin/pip" install --quiet pydantic
    echo "    pydantic installe"
    echo ""
done

# 2. Generation des donnees de test
echo ">>> Generation des donnees de test"
cd tools
python3 data_exporter.py > /dev/null 2>&1
cd ..
echo "    Donnees disponibles dans tools/generated_data/"
echo ""

# 3. Recapitulatif
echo "======================================"
echo "  Setup termine"
echo "======================================"
echo ""
echo "Pour lancer les demos officielles :"
echo "  ex0/venv/bin/python ex0/space_station.py"
echo "  ex1/venv/bin/python ex1/alien_contact.py"
echo "  ex2/venv/bin/python ex2/space_crew.py"
echo ""
echo "Pour lancer les tests batch bonus :"
echo "  ex0/venv/bin/python tests/test_ex0.py"
echo "  ex1/venv/bin/python tests/test_ex1.py"
echo "  ex2/venv/bin/python tests/test_ex2.py"
echo ""
