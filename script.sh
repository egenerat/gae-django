cd tests_util/
tar zvf test_pages.tar
docker build -t fm/webserver_test_pages .
docker run -d fm/webserver_test_pages
export WEBSERVER_TEST_PAGES_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' webserver_test_pages)
cd ..
