#!/bin/bash
#crear directorio de output necesario para helm 
mkdir -p output/helm

echo "Generando manifiestos con nuestra app-generator..."
python src/manifest_generator.py \
  -t templates/service.yaml.template templates/deployment.yaml.template \
  -v templates/values.yaml \
  -o output/app-generator/

echo "Generando manifiestos con helm..."
helm template my-app ./helm-chart/app-chart/ \
  -s templates/deployment.yaml > output/helm/deployment.yaml

helm template my-app ./helm-chart/app-chart/ \
  -s templates/service.yaml > output/helm/service.yaml

echo "Comparando manifiestos generados con diff..."
echo "=== deployment diff ==="
diff output/app-generator/deployment.yaml output/helm/deployment.yaml

echo "=== service diff ==="  
diff output/app-generator/service.yaml output/helm/service.yaml
