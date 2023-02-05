use std::str::FromStr;

use std::net::Ipv4Addr;

fn get_subnet_range(ip_cidr: &str) -> (String, String, String) {
    let mut parts = ip_cidr.split("/");
    let ip = parts.next().unwrap();
    let cidr = parts.next().unwrap();
    let ip = Ipv4Addr::from_str(ip).unwrap();
    let cidr = cidr.parse::<u8>().unwrap();
    let mask = 32 - cidr;
    let subnet = Ipv4Addr::new(!0, !0, !0, !0 << mask);
    let last_ip = Ipv4Addr::new(
        ip.octets()[0] | !(!0 << mask),
        ip.octets()[1] | !(!0 << mask),
        ip.octets()[2] | !(!0 << mask),
        ip.octets()[3] | !(!0 << mask),
    );
    let first_ip = ip;
    (subnet.to_string(), last_ip.to_string(), first_ip.to_string())
}

fn main() {
    let ip_cidr = "192.168.56.0/21";
    let (subnet, last_ip, first_ip) = get_subnet_range(ip_cidr);
    println!("Subnet mask: {}", subnet);
    println!("Last IP: {}", last_ip);
    println!("First IP: {}", first_ip);
}
