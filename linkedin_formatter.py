def format_linkedin_data(data):
    formatted_data = {}

    formatted_data['Company Name'] = data.get('name', 'N/A')
    formatted_data['Tagline'] = data.get('tagline', 'N/A').strip()
    formatted_data['Description'] = data.get('description', 'N/A')
    formatted_data['Website'] = data.get('callToAction', {}).get('url', 'N/A')
    formatted_data['Staff Count'] = data.get('staffCount', 'N/A')
    formatted_data['Industries'] = [industry['localizedName'] for industry in data.get('companyIndustries', [])]

    formatted_data['Affiliated Companies'] = []
    for urn, company_data in data.get('affiliatedCompaniesResolutionResults', {}).items():
        company_info = {
            'Name': company_data.get('name', 'N/A'),
            'Description': company_data.get('description', 'N/A'),
            'Website': company_data.get('url', 'N/A'),
            'Followers': company_data.get('followingInfo', {}).get('followerCount', 'N/A'),
            'Industries': [industry['localizedName'] for industry in company_data.get('companyIndustries', [])]
        }
        formatted_data['Affiliated Companies'].append(company_info)

    formatted_data['Specialties'] = data.get('specialities', [])

    confirmed_locations = data.get('confirmedLocations', [])
    if confirmed_locations:
        formatted_data['Headquarters'] = confirmed_locations[0]
    else:
        formatted_data['Headquarters'] = {'city': 'N/A', 'country': 'N/A'}

    return formatted_data

def display_linkedin_data(data):
    formatted_data = format_linkedin_data(data)

    print(f"Company Name: {formatted_data['Company Name']}")
    print(f"Tagline: {formatted_data['Tagline']}")
    print(f"Description: {formatted_data['Description']}")
    print(f"Website: {formatted_data['Website']}")
    print(f"Staff Count: {formatted_data['Staff Count']}")
    print(f"Industries: {', '.join(formatted_data['Industries'])}")
    print("\nAffiliated Companies:")
    for company in formatted_data['Affiliated Companies']:
        print(f"  - Name: {company['Name']}")
        print(f"    Description: {company['Description']}")
        print(f"    Website: {company['Website']}")
        print(f"    Followers: {company['Followers']}")
        print(f"    Industries: {', '.join(company['Industries'])}")
    print(f"\nSpecialties: {', '.join(formatted_data['Specialties'])}")
    print(f"Headquarters: {formatted_data['Headquarters']['city']}, {formatted_data['Headquarters']['country']}")
