# demo_microservices_flask
has three microservices (User, Product, Orders)

# Quick Start
git clone https://github.com/dkoh-pub/demo_microservices_flask.git
# Enter directory
cd ~/demo_microservices_flask
# Run docker
docker compose up -d

#test API
curl -i http://localhost:5001/api/v1/users
