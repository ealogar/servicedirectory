#!/bin/bash
echo "=== Starting sanity check ==="
read -p "Enter IP:PORT : " host
echo
echo "Creating a class..."
curl -H 'Authorization: Basic YWRtaW46YWRtaW4=' -H 'Origin: http://$host' -X POST --data 'class_name=ClassTest&default_version=1.0&description=Description' http://$host/sd/v1/classes
echo
echo "Creating an instance..."
curl --header 'Authorization: Basic YWRtaW46YWRtaW4=' -X POST --data 'environment=production&class_name=ClassTest&version=v1.0&url=http://instance_client0.tid.es' http://$host/sd/v1/classes/ClassTest/instances/
echo
read -p "Enter Instance Id : " instance
echo
echo "Creating a binding..."
curl --header 'Authorization: Basic YWRtaW46YWRtaW4=' -X POST -H "Accept: application/json" -H "Content-type: application/json" -d '{"origin": "Client0", "class_name": "ClassTest", "binding_rules": [{"group_rules": [{"operation": "range", "input_context_param": "param_1", "value": [1, 100]}], "bindings": ["'"$instance"'"]}]}' http://$host/sd/v1/bindings
echo
read -p "Enter Binding Id : " binding
echo
echo "Searching the binding..."
curl --header 'Authorization: Basic YWRtaW46YWRtaW4=' "http://$host/sd/v1/bind_instances?class_name=ClassTest&version=v1.0&origin=Client0&param_1=5"
echo
echo "Delete the binding..."
curl --header 'Authorization: Basic YWRtaW46YWRtaW4=' -X DELETE -H "Accept: application/json" -H "Content-type: application/json" http://$host/sd/v1/bindings/$binding
echo
echo "Delete the instance..."
curl --header 'Authorization: Basic YWRtaW46YWRtaW4=' -X DELETE http://$host/sd/v1/classes/ClassTest/instances/$instance
echo
echo "Delete the class..."
curl -H 'Authorization: Basic YWRtaW46YWRtaW4=' -H 'Origin: http://$host' -X DELETE http://$host/sd/v1/classes/ClassTest
echo
echo "=== Sanity check finished ==="
