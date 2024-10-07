class NetIPv4:
    def __init__(self, ip):
        """
        Inicializace třídy. Zajišťuje validaci a zpracování IP adresy.
        """
        try:
            self.ip, self.prefixlen = self._parse_ip(ip)
            self.mask = self._calculate_netmask(self.prefixlen)
            self.network = self._calculate_network_address(self.ip, self.mask)
        except ValueError as e:
            raise ValueError(str(e))
    
    def _parse_ip(self, ip):
        """
        Ověřuje a vrací IP adresu a délku prefixu. Pokud není prefix zadán, 
        zvolí se defaultní maska podle třídy IP adresy (A, B, C).
        """
        try:
            if '/' in ip:
                ip_part, prefix_part = ip.split('/')
                prefixlen = int(prefix_part)
            else:
                ip_part = ip
                # Zvolí výchozí délku prefixu podle třídy IP adresy
                prefixlen = self._get_default_prefix(ip_part)
            
            if prefixlen < 0 or prefixlen > 32:
                raise ValueError("Neplatná délka prefixu.")
            
            ip_octets = ip_part.split('.')
            
            if len(ip_octets) != 4:
                raise ValueError("Neplatný formát IP adresy.")
            
            ip_bytes = [int(octet) for octet in ip_octets]
            
            if any(octet < 0 or octet > 255 for octet in ip_bytes):
                raise ValueError("Oktet IP adresy musí být mezi 0 a 255.")
            
            return ip_bytes, prefixlen
        except ValueError:
            raise ValueError("Neplatná IPv4 adresa.")
    
    def _get_default_prefix(self, ip):
        """
        Vrací výchozí délku prefixu (masku) na základě třídy IP adresy.
        """
        first_octet = int(ip.split('.')[0])
        if first_octet >= 1 and first_octet <= 126:  # Třída A
            return 8
        elif first_octet >= 128 and first_octet <= 191:  # Třída B
            return 16
        elif first_octet >= 192 and first_octet <= 223:  # Třída C
            return 24
        else:
            raise ValueError("Nepodporovaná IP adresa. Podporované jsou třídy A, B, C.")
    
    def _calculate_netmask(self, prefixlen):
        """
        Vypočítá masku sítě na základě délky prefixu.
        """
        mask = [0, 0, 0, 0]
        for i in range(32):
            if i < prefixlen:
                mask[i // 8] += (1 << (7 - i % 8))
        return mask
    
    def _calculate_network_address(self, ip, mask):
        """
        Vypočítá adresu sítě pomocí IP adresy a masky.
        """
        return [ip[i] & mask[i] for i in range(4)]
    
    def _calculate_broadcast_address(self):
        """
        Vypočítá broadcast adresu na základě IP a masky.
        """
        inverted_mask = [~m & 0xFF for m in self.mask]
        return [self.network[i] | inverted_mask[i] for i in range(4)]
    
    def _is_private(self):
        """
        Zjistí, zda je IP adresa privátní.
        """
        if (self.ip[0] == 10 or 
            (self.ip[0] == 172 and 16 <= self.ip[1] <= 31) or 
            (self.ip[0] == 192 and self.ip[1] == 168)):
            return True
        return False
    
    def get_ip_info(self):
        """
        Vrací základní informace o IP adrese, jako je IP, maska, prefix, zda je privátní, atd.
        """
        print(f"\n--- Informace o IP adrese {'.'.join(map(str, self.ip))}/{self.prefixlen} ---")
        print(f"Adresa: {'.'.join(map(str, self.ip))}")
        print(f"Typ IP: IPv4")
        print(f"Maska sítě: {'.'.join(map(str, self.mask))}")
        print(f"Prefix délka: {self.prefixlen}")
        print(f"Je privátní: {self._is_private()}")
        print(f"Je veřejná: {not self._is_private()}")
    
    def get_broadcast_info(self):
        """
        Vrací informace o broadcast adrese a maximálním počtu hostů v síti.
        """
        broadcast = self._calculate_broadcast_address()
        max_hosts = (2 ** (32 - self.prefixlen)) - 2
        print(f"Broadcast adresa: {'.'.join(map(str, broadcast))}")
        print(f"Maximální počet hostů: {max_hosts}")
    
    def get_address_range(self):
        """
        Vrací rozsah adres v síti (od první do poslední).
        """
        first_address = self.network[:]
        first_address[-1] += 1
        broadcast = self._calculate_broadcast_address()
        last_address = broadcast[:]
        last_address[-1] -= 1
        print(f"Rozsah adresy: {'.'.join(map(str, first_address))} - {'.'.join(map(str, last_address))}")
    
    def get_network_address(self):
        """
        Vrací síťovou adresu.
        """
        print(f"Síťová adresa: {'.'.join(map(str, self.network))}")

# Hlavní část programu
if __name__ == "__main__":
    ip_input = input("Zadejte IPv4 adresu (např. 192.168.1.1): ")
    
    try:
        net_ip = NetIPv4(ip_input)
        net_ip.get_ip_info()
        net_ip.get_broadcast_info()
        net_ip.get_address_range()
        net_ip.get_network_address()
    
    except ValueError as e:
        print(e)
