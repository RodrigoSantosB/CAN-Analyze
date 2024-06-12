from attacks import CanAttack 


if __name__ == "__main__":
    can_at = CanAttack()
    
    input = ('input attck')
    
    if input == 'fuzzy':
        can_at.send_fuzzy_attack()
    if input == 'masquerade':
        can_at.send_masquerade_attack()
    if input == 'spoofed':
        can_at.send_spoofed_attack()
    if input == 'dos':
        can_at.send_dos_attack()