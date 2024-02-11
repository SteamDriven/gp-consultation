import textwrap


def format_paragraph(input_string, width):
    if len(input_string) < width:  # Adjust the threshold as needed
        return input_string
    else:
        return textwrap.fill(input_string, width=width)


# Short message
short_message = "This is a short message."

# Long message
long_message = (f"You have scheduled a request for an appointment with Dr "
                f"John A. Doe. "
                f"The appointment is set for Thursday 18 Feb at Morning.\n"
                f"You will receive a confirmation upon acceptance of your appointment.")

width = 120

formatted_short = format_paragraph(short_message, width)
formatted_long = format_paragraph(long_message, width)

print(f"Formatted Short Message:\n{formatted_short}\n" + '-' * 40)
print(f"Formatted Long Message:\n{formatted_long}\n" + '-' * 40)
