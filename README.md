Settings:
  set your email in 'settings.py' file
  set your production env in 'envs/pro_env' if need

Deploy:
  //enter the directory
  cd backend

  //build docker in development env
  docker build --tag ee_shopping .

  //build docker in production env
  docker build --tag ee_shopping . --build-arg DJANGO_ENV=production

  //run docker in development env
  docker run -d -p8000:8000 --name ee_shopping ee_shopping

  //run docker in production env
  docker run -d -p8000:8000 --name ee_shopping -e DJANGO_ENV=production ee_shopping

  //start/stop docker
  docker start/stop ee_shopping

  //each time update docker
  docker stop ee_shopping
  docker rm ee_shopping
  docker rmi ee_shopping
  docker build --tag ee_shopping .
  docker run -d -p8000:8000 --name ee_shopping ee_shopping
  or
  docker build --tag ee_shopping . --build-arg DJANGO_ENV=production
  docker run -d -p8000:8000 --name ee_shopping -e DJANGO_ENV=production ee_shopping

Database Maintain:
  //It is necessary to clean up the data of expired tokens from time to time!!!
  DELETE FROM token_blacklist_blacklistedtoken
  WHERE token_id IN (
      SELECT id FROM token_blacklist_outstandingtoken
      WHERE expires_at < NOW()
  );
  DELETE FROM token_blacklist_outstandingtoken
  WHERE expires_at < NOW();