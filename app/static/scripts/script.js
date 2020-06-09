function BlurInput(input)
{
    if (input.value == "")
    {
        input.style.backgroundColor = "#ffcc66";                
        return false;
    }
    else
    {
        input.style.backgroundColor = "white";                
    }
}
function FocusInput(input)
{
    if (input.value == "")
    {
        input.style.backgroundColor = "#b3d9ff";                
        return false;
    }
    else
    {
        input.style.backgroundColor = "white";                
    }
}