#!/bin/bash
export ANSIBLE_HOST_KEY_CHECKING=False
ansible-playbook -vv -i hosts ansible.yaml -e "SNOW_SECRET_KEY=$SNOW_SECRET_KEY SNOW_SQLALCHEMY_DATABASE_URI=$SNOW_SQLALCHEMY_DATABASE_URI image_tag=$IMAGE_TAG"
