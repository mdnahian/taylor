
import json
import language_check
from os.path import join, dirname
from watson_developer_cloud import AlchemyLanguageV1



fillers = ['like', 'umm', 'ah', 'you know', 'ok so']

tool = language_check.LanguageTool('en-US')



def execute(raw):

	num_filler_words = 0
	num_grammatical_errors = 0

	raw_sections = json.loads(raw)

	sections = raw_sections['sections']
	


	result = '''
		{ 
			"sections": [
	'''



	for i in range(0, len(sections)):

		section = sections[i]

		question = section['question']
		response = section['response']

		result += '''
			{
				"question":"'''+question+'''",
				"response":"'''+response+'''",
		'''

		sentences = response.split('.')

		new_response = ''

		result += '''
					"grammatical_errors": [
		'''
	
		for sentence in sentences:

			sentence = sentence.strip()

			# num_filler_words_in_response = 0

			for filler_word in fillers:
				if filler_word in sentence:
					num_filler_words += 1
					# num_filler_words_in_response += 1
					sentence.replace(filler_word, '')

			new_response += sentence + '. '

			grammer_matches = tool.check(sentence)


			if len(grammer_matches) > 0:

				result += '''
					{
				'''

				num_grammatical_errors += len(grammer_matches)


				result += '''
								"errors": [
						'''

				for i in range(0, len(grammer_matches)):
				 
					result += '''
						{
							"suggestion":"'''+grammer_matches[i].msg+'''",
							"replacements":"'''+''.join(grammer_matches[i].replacements)+'''"
						}
					'''

					if i < len(grammer_matches) - 1:
						result += ','

				

				result += '''
						],
						"sentence":"'''+sentence+'''",
						"corrected":"'''+language_check.correct(sentence.strip(), grammer_matches)+'''"
					}
				'''


		result += '''
				],
		'''

		raw_text_analytics = getTextAnalytics(new_response)

		result += '''
			"response_sentiment": {
				"score": "'''+raw_text_analytics['docSentiment']['score']+'''",
				"type": "'''+raw_text_analytics['docSentiment']['type']+'''"
			},
			"emotions": {
				"anger": "'''+raw_text_analytics['docEmotions']['anger']+'''", 
			    "joy": "'''+raw_text_analytics['docEmotions']['joy']+'''", 
			    "fear": "'''+raw_text_analytics['docEmotions']['fear']+'''", 
			    "sadness": "'''+raw_text_analytics['docEmotions']['sadness']+'''", 
			    "disgust": "'''+raw_text_analytics['docEmotions']['disgust']+'''"
			}
		'''


		result += '''
			}
		'''


		if i < len(sections) - 1:
			result += ','


	result += '''
			],
			"stats": {
				"num_filler_words": '''+str(num_filler_words)+''',
				"num_grammatical_errors": '''+str(num_grammatical_errors)+'''
			}
		}
	'''


	return result.encode('ascii', 'ignore').decode('ascii')








def getTextAnalytics(text):

	alchemy_language = AlchemyLanguageV1(api_key='bef063351ecbc10dfc4baea5077310fa18d439fd')

	combined_operations = ['entity', 'keyword', 'concept', 'doc-emotion', 'doc-sentiment']

	return alchemy_language.combined(text=text, extract=combined_operations)



# with open('example.json', 'r') as json_file:
# 	data = json_file.read()

# print execute(data)



