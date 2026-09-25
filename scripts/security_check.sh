#!/bin/bash
# ============================================
# Vérification de sécurité pré-push
# Usage : bash scripts/security_check.sh
# ============================================

echo "🔒 Vérification de sécurité pré-push"
echo "======================================"

FAIL=0

# 1. Fichiers data dans le staging
if git diff --cached --name-only 2>/dev/null | grep -qE '\.(csv|parquet|xlsx|json|h5|pkl|pt|pth|joblib)$'; then
    echo "❌ Fichiers data/modèles détectés dans le staging :"
    git diff --cached --name-only | grep -E '\.(csv|parquet|xlsx|json|h5|pkl|pt|pth|joblib)$'
    FAIL=1
else
    echo "✓ Pas de fichier data/modèle dans le staging"
fi

# 2. Chemins absolus
if grep -rn 'C:\\Users\|/home/\|/Users/' --include="*.py" --include="*.ipynb" . 2>/dev/null | grep -v ".gitignore" | grep -v "security_check"; then
    echo "❌ Chemins absolus détectés (voir ci-dessus)"
    FAIL=1
else
    echo "✓ Pas de chemin absolu détecté"
fi

# 3. Clés API
if grep -rnE '(sk-[a-zA-Z0-9]{20,}|api_key\s*=\s*['\''"][^'\''"]+['\''"]|token\s*=\s*['\''"][^'\''"]+['\''"])' --include="*.py" --include="*.ipynb" . 2>/dev/null; then
    echo "❌ Clé API potentielle détectée (voir ci-dessus)"
    FAIL=1
else
    echo "✓ Pas de clé API détectée"
fi

# 4. .gitignore
if [ ! -f .gitignore ]; then
    echo "❌ Pas de .gitignore"
    FAIL=1
else
    echo "✓ .gitignore présent"
fi

# 5. Fichiers volumineux (> 10 Mo)
LARGE_FILES=$(find . -name ".git" -prune -o -type f -size +10M -print 2>/dev/null)
if [ -n "$LARGE_FILES" ]; then
    echo "⚠️  Fichiers > 10 Mo trouvés (vérifier qu'ils sont gitignored) :"
    echo "$LARGE_FILES"
else
    echo "✓ Pas de fichier volumineux non-git"
fi

echo "======================================"
if [ $FAIL -eq 0 ]; then
    echo "✅ Tout est bon, tu peux push !"
else
    echo "⚠️  Corrige les problèmes avant de push."
    exit 1
fi
