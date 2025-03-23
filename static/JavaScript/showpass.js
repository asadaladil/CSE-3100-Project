document.getElementById('id_Check').addEventListener('change', function() 
{
    const pass1Field = document.getElementById('id_password1');
    const pass2Field = document.getElementById('id_password2');
    const pass3Field = document.getElementById('id_Password');
    if (this.checked) 
    {
        pass1Field.type = 'text';
        pass2Field.type = 'text';
        pass3Field.type = 'text';
    } 
    else 
    {
        pass1Field.type = 'password';
        pass2Field.type = 'password';
        pass3Field.type = 'password';
    }
});