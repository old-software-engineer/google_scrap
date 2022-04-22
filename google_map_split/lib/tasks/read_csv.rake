require 'csv'
namespace :csvvv do
  desc "Spliting table"
  task read: :environment do
  	@count = 0
  	def print_the_records(contacts_array)
  		contacts_array.each do |contact|
  			puts @count
  			@count +=1
  		end
  	end
  	system 'mkdir file'
  	system 'cd ./file && wget https://docs.google.com/spreadsheets/d/1tIATmDHU-AAocQFOZgaNYOKhMUnPNxOZd8DaSJauj0Q/export?format=csv'
  	file = File.read('./file/export?format=csv')
  	file_csv = CSV.parse(file, headers: true)
  	min = 0
  	max = 1000
  	total_count = file_csv.count

  	contact_bundle1000 = []
  	while max<=total_count do 
  		print_the_records(file_csv[min .. max-1])
  		min += 1000
  		max += 1000
  	end
  	remainder = total_count % 1000
  	if remainder > 0
  		print_the_records(file_csv[min .. min+remainder-1])
  	end
  	system 'rm -f ./file/export?format=csv &&  rmdir file'
  end
end