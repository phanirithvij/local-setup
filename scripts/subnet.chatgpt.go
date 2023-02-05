package main

import (
	"fmt"
	"net"
)

func getSubnetRange(ipCIDR string) (string, string, string) {
	// Create an IPNet object from the IP address and CIDR notation
	ip, ipnet, err := net.ParseCIDR(ipCIDR)
	if err != nil {
		fmt.Println(err)
	}
	// Get the subnet mask
	subnet := []byte(ipnet.Mask)
	// Get the last IP address in the subnet
	lastIP := make([]byte, len(subnet))
	ip = ip.To4()
	for i := range lastIP {
		lastIP[i] = ip[i] | ^subnet[i]
	}
	// Get the first IP address in the subnet
	firstIP := ipnet.IP
	subnetString := fmt.Sprintf("%v.%v.%v.%v", subnet[0], subnet[1], subnet[2], subnet[3])
	return subnetString, net.IP(lastIP).String(), firstIP.String()
}

func main() {
	ipCIDR := "192.168.56.0/21"
	subnet, lastIP, firstIP := getSubnetRange(ipCIDR)
	fmt.Println("IP CIRD:", ipCIDR)
	fmt.Println("First IP:", firstIP)
	fmt.Println("Subnet mask:", subnet)
	fmt.Println("Last IP:", lastIP)
}
