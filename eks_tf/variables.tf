#general

variable "region" {
  type    = string
  default = "eu-central-1"
}

#eks cluster

variable "cluster_name" {
  type    = string
  default = "EKS_Cluster"
}

variable "cluster_version" {
  type    = string
  default = "1.31"
}


#tags

variable "environment" {
  type    = string
  default = "dev"
}


#vpc

variable "vpc_id" {
  type    = string
  default = "vpc-06774b48185afd13e"
}

variable "subnet_ids" {
  type    = list(string)
  default = ["subnet-00f1755062a63efa9", "subnet-02d5fdeff0a8c5560", "subnet-0755b2fb744870b52"]
}

#node groups

variable "instance_types" {
  type    = list(string)
  default = ["t2.micro"]
}
