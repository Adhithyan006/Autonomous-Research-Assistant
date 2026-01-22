topic = input("Enter your research topic: ")

content = f"""
{topic} is a critical area of study with increasing importance.

It influences industry, technology, and research practices.
It provides benefits but also raises challenges.
"""

summary = f"""
Summary:
{topic} has strong relevance today.
Careful design and evaluation are required.
"""

length = len(topic)

if length < 15:
    confidence = "Low"
    risk = "High risk"
elif length < 30:
    confidence = "Medium"
    risk = "Moderate risk"
else:
    confidence = "High"
    risk = "Low risk"

print("\n--- Research Content ---")
print(content)

print("\n--- Summary ---")
print(summary)

print("\n--- Analysis ---")
print("Confidence:", confidence)
print("Risk:", risk)
