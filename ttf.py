import math

class cls:
	pass

def getUint(fp, offset, numOfBytes):
	fp.seek(offset)
	ret = 0
	for i in xrange(numOfBytes):
		ret = (ret << 8) + ord(fp.read(1))
	return ret

def getUint32(fp, offset):
	return getUint(fp, offset, 4)

def getUint16(fp, offset):
	return getUint(fp, offset, 2)

def getUint8(fp, offset):
	return getUint(fp, offset, 1)

def getFixed(fp, offset):
	val = getUint32(fp, offset)
	return math.ceil(val / 65536.0)

def getString(fp, num, offset):
	fp.seek(offset)
	return fp.read(num)

def padZero(ch, width):
	return ("0000000000000000000000000000000000000000000000000000000000000000" + ch)[-1 * width:]

def getInt(fp, offset, numOfBytes):
	fp.seek(offset)
	ret = 0
	for i in xrange(numOfBytes):
		ret = (ret << 8) + ord(fp.read(1))
	if ret & 1 << (numOfBytes * 8 - 1):
		ret = ret - (1 << (numOfBytes * 8))
	return ret

def getInt16(fp, offset):
	return getInt(fp, offset, 2)

class TTFTableDirecotry:
	def __init__(self, fp, offset, numTables):
		self.item = {}
		l = numTables * 16
		for i in xrange(offset, l, 16):
			tag = getString(fp, 4, i)
			checkSum = padZero(hex(getUint32(fp, i + 4))[2:], 8)
			offset = getUint32(fp, i + 8)
			length = getUint32(fp, i + 12)
			self[tag] = {
				"tag" : tag,
				"checkSum" : checkSum,
				"offset" : offset,
				"length" : length,
			}
			pass
		pass

	def __setitem__(self, key, value):
		self.item[key] = value
		pass

	def __getitem__(self, key):
		return self.item[key]

class TTFGlyf:
	def __init__(self, fp, offset, isNull):
		self.offset = offset
		self.isNull = isNull
		self.flags = []
		self.flagsOrig = []
		self.totalOfCoordinates = 0
		self.coordinates = []
		self.xCoorinateOffset = 0
		self.xCoordinates = []
		self.yCoorinateOffset = 0
		self.yCoordinates = []
		self.pathArray = []
		self.path = ""

		if not isNull:
			self.init(fp, offset)
			pass
		pass

	def init(self, fp, offset):
		self.numberOfContours = getInt16(fp, offset)
		offset += 2
		self.xMin = getInt16(fp, offset)
		offset += 2
		self.yMin = getInt16(fp, offset)
		offset += 2
		self.xMax = getInt16(fp, offset)
		offset += 2
		self.yMax = getInt16(fp, offset)
		offset += 2

		self.endPtsOfContours = []
		if self.numberOfContours >= 0:
			for i in xrange(self.numberOfContours):
				self.endPtsOfContours.append(getUint16(fp, offset))
				offset += 2
				pass
			pass

		self.instructionLength = getUint16(fp, offset)
		offset += 2
		self.instructions = []
		for i in xrange(self.instructionLength):
			offset += 1
			pass

		self.flagsOffset = offset
		# self._readGlyfCoordinates()
		pass

	# def readGlyfCoordinates:
	# 	if self.numberOfContours >= 0:
	# 		self._readSimpleGlyf()
	# 		pass
	# 	pass

	# def _readSimpleGlyf:
	# 	offset = self.flagsOffset

	# 	totalOfCoordinates = self.endPtsOfContours[len(self.endPtsOfContours) - 1] + 1
	# 	self.totalOfCoordinates = totalOfCoordinates

	# 	i = 0
	# 	while i < totalOfCoordinates:
	# 		flag = getUint8(fp, offset)
	# 		self.flags.append(flag)
	# 		offset++
	# 		i++

	# 		if flag & 8 and i < totalOfCoordinates:
	# 			repeat = getUint8(fp, offset)
	# 			offset++
	# 			self.flagsOrig.append(repeat)
	# 			for j in xrange(repeat):
	# 				self.flags.append(flag)
	# 				i++
	# 				pass
	# 			pass
	# 		pass

	# 	self.xCoorinateOffset = offset
	# 	prevX = 0
	# 	for i in range(self.flags.length):
	# 		x = 0
	# 		flag = self.flags[i]

	# 		if flag & 2:
	# 			x = getUint8(fp, offset)
	# 			offset += 1
	# 			x = (flag & 16) ? x : -1 * x
	# 		elif flag & 16:
	# 			x = 0
	# 		else:
	# 			x = getInt16(fp, offset)
	# 			offset += 2
	# 			pass

	# 		prevX += x
	# 		self.xCoordinates[i] = prevX
	# 		self.coordinates[i] = {
	# 			"x" : prevX,
	# 			"y" : 0,
	# 			"isOnCurve" : Boolean(flag & 1)
	# 		}
	# 	}

	# 	self.yCoorinateOffset = offset
	# 	prevY = 0
	# 	for i in xrange(len(self.flags):
	# 		y = 0
	# 		flag = self.flags[i]

	# 		if flag & 4:
	# 			y = getUint8(fp, offset)
	# 			offset++
	# 			y = y if (flag & 32) else -1 * y
	# 		elif flag & 32:
	# 			y = 0
	# 		else:
	# 			y = getInt16(fp, offset)
	# 			offset += 2
			
	# 		prevY += y
	# 		self.yCoordinates[i] = prevY
	# 		if self.coordinates.has_key(i):
	# 			self.coordinates[i].y = prevY
	# 			pass
	# 		pass

	# 	pathArray = []
	# 	startPts = 0

	# 	endPts = self.endPtsOfContours[i]
	# 	for i in xrange(len(self.endPtsOfContours):
	# 		try {
	# 			for currentPts in xrange(endPts + 1):
	# 				path = ""
	# 				currentPoint = self.coordinates[currentPts]
	# 				prevPoint = self.coordinates[endPts] if (currentPts == startPts) else self.coordinates[currentPts - 1]
	# 				nextPoint = self.coordinates[startPts] if (currentPts == endPts) else self.coordinates[currentPts + 1]

	# 				if (typeof currentPoint === 'undefined') {
	# 					continue
	# 				}

	# 				if (currentPts === startPts) { 						if (currentPoint.isOnCurve) {
	# 						path += "M" + currentPoint.x + "," + currentPoint.y
	# 								+ " "
	# 					} else { 
	# 													midPoint = {
	# 							x : (prevPoint.x + currentPoint.x) / 2,
	# 							y : (prevPoint.y + currentPoint.y) / 2
	# 						}
	# 						path += "M" + midPoint.x + "," + midPoint.y + " Q"
	# 								+ currentPoint.x + "," + currentPoint.y
	# 								+ " "
	# 					}
	# 				} else {
	# 											if (typeof currentPoint !== 'undefined'
	# 							&& typeof currentPoint.isOnCurve === 'boolean'
	# 							&& currentPoint.isOnCurve
	# 							&& typeof prevPoint !== 'undefined'
	# 							&& typeof prevPoint.isOnCurve === 'boolean'
	# 							&& prevPoint.isOnCurve) { 							path += " L"
	# 					} else if (currentPoint.isOnCurve === false
	# 							&& typeof prevPoint !== 'undefined'
	# 							&& typeof prevPoint.isOnCurve === 'boolean'
	# 							&& prevPoint.isOnCurve === false) { 
	# 													midPoint = {
	# 							x : (prevPoint.x + currentPoint.x) / 2,
	# 							y : (prevPoint.y + currentPoint.y) / 2
	# 						}
	# 						path += midPoint.x + "," + midPoint.y + " "
	# 					} else if (!currentPoint.isOnCurve) { 							path += " Q"
	# 					}

	# 											path += currentPoint.x + "," + currentPoint.y + " "
	# 				}
	# 				pathArray.append(path)
	# 			}

	# 							if (!currentPoint.isOnCurve
	# 					&& typeof self.coordinates[startPts] !== 'undefined') {

	# 								  if (self.coordinates[startPts].isOnCurve) {
	# 					pathArray.append(self.coordinates[startPts].x + ","
	# 							+ self.coordinates[startPts].y + " ")
	# 				} else {
	# 					midPoint = {
	# 							x : (currentPoint.x + self.coordinates[startPts].x) / 2,
	# 							y : (currentPoint.y + self.coordinates[startPts].y) / 2
	# 						}
	# 					pathArray.append(midPoint.x + "," + midPoint.y + " ")
	# 				}
	# 			}

	# 							pathArray.append(" Z ")

	# 							startPts = self.endPtsOfContours[i] + 1
	# 		} catch (e) {
	# 							console.log(e)
	# 			console.log(currentPoint, prevPoint, nextPoint, self.
	# 		}
	# 	}
	# 	self.pathArray = pathArray
	# 	self.path = pathArray.join(" ")
	# }

class TTFCmap:

	def __init__(self, fp, offset):
		self.item = {}
		self.format = getUint16(fp, offset)
		if getattr(self, '_initFormat' + str(self.format)):
			getattr(self, '_initFormat' + str(self.format))(fp, offset)
			pass
		else:
			raise 'Not support cmap format' + format + ' yet! Please submit an issue at github'
			pass
		pass

	def __setitem__(self, key, value):
		self.item[key] = value
		pass

	def __getitem__(self, key):
		return self.item[key]

	def _initFormat0(self, fp, offset):
		self["length"] = getUint16(fp, offset+2)
		self["language"] = getUint16(fp, offset+4)
		self["glyphIndexArray"] = []
		self["offset"] = offset
		for i in xrange(6, self["length"]):
			self["glyphIndexArray"].append(getUint8(fp, offset + i))
			pass

		def _getGlyphIndex(ch):
			code = ord(ch)
			return self["glyphIndexArray"][code] if code < 256 else 0
		self._getGlyphIndex = _getGlyphIndex

		def _getGlyphIndexs():
			return self["glyphIndexArray"]
		self._getGlyphIndexs = _getGlyphIndexs

		pass

	def _getGlyphIndex(self):

		pass

	def _initFormat4(self, fp, offset):
		self["length"] = getUint16(fp, offset+2)
		self["language"] = getUint16(fp, offset+4)
		self["segCount"] = getUint16(fp, offset + 6 )/2
		self["searchRange"] = getUint16(fp, offset + 8 )
		self["entrySelector"] = getUint16(fp, offset + 10)
		self["rangeShift"] = getUint16(fp, offset + 12 )

		self["endCode"] = []
		self["startCode"] = []
		self["idDelta"] = []
		self["idRangeOffset"] = []
		for i in xrange(self["segCount"]):
			self["endCode"].append(getUint16(fp, offset + 14 + 2*i))
			self["startCode"].append(getUint16(fp, offset + 16 + self["segCount"]*2 + 2*i))
			self["idDelta"].append(getInt16(fp, offset + 16 + self["segCount"]*4 + 2*i))
			self["idRangeOffset"].append(getUint16(fp, offset + 16 + self["segCount"]*6 + 2*i))
			pass
		self["reservedPad"] = getUint16(fp, offset + 14 + self["segCount"] * 2)

		self["glyphIndexArray"] = []
		for i in xrange(offset + 16 + self["segCount"]*8, offset + self["length"], 2):
			self["glyphIndexArray"].append(getUint16(fp, i))
			pass

		def _getGlyphIndex(ch):
			code = ord(ch)
			segmentIndex = 0
			for index, item in enumerate(self["endCode"]):
				if code <= item:
					segmentIndex = index
					break
				pass
			idRangeOffset = self["idRangeOffset"][segmentIndex]
			idDelta = self["idDelta"][segmentIndex]
			startCode = self["startCode"][segmentIndex]
			endCode = self["endCode"][segmentIndex]

			if idRangeOffset == 0:
				if code >= startCode and code <= endCode:
					code += idDelta
					print(code)
					return code
				else:
					return 0
				pass
			else:
				raise 'Not support cmap format4 with idRangeOffset is not zero yet! Please submit an issue at github'
				pass
			pass
		self._getGlyphIndex = _getGlyphIndex
		pass
	pass

class TTF:

	def __init__(self, fontfile):
		self.fontfile = fontfile
		self.item = {}
		pass

	def __setitem__(self, key, value):
		self.item[key] = value
		pass

	def __getitem__(self, key):
		return self.item[key]

	def readTables(self):
		with open(self.fontfile, "rb") as fp:
			self.version = getFixed(fp, 0)
			self.numTables = getUint16(fp, 4)
			self.searchRenge = getUint16(fp,6)
			self.entrySelector = getUint16(fp, 8)
			self.rengeShift = getUint16(fp, 10)
			self.tableDirectory = TTFTableDirecotry(fp, fp.tell(), self.numTables)
			for tag in self.tableDirectory.item:
				self[tag] = {}
				pass

			# head
			headOffset = self.tableDirectory["head"]["offset"]
			self["head"] = {}
			self["head"]["version"] = getFixed(fp, headOffset)
			self["head"]["fontRevision"] = getFixed(fp, headOffset + 4)
			self["head"]["checkSumAdjustment"] = hex(getUint32(fp, headOffset + 8))[2:]
			self["head"]["magickNumber"] = hex(getUint32(fp, headOffset + 12))[2:]
			self["head"]["flags"] = padZero(bin(getUint16(fp, headOffset + 16))[2:], 16)
			self["head"]["unitsPerEm"] = getUint16(fp, headOffset + 18)
			self["head"]["xMin"] = getInt16(fp, headOffset + 36)
			self["head"]["yMin"] = getInt16(fp, headOffset + 38)
			self["head"]["xMax"] = getInt16(fp, headOffset + 40)
			self["head"]["yMax"] = getInt16(fp, headOffset + 42)
			self["head"]["macStyle"] = padZero(bin(getUint16(fp, headOffset + 44))[2:], 16)
			self["head"]["lowestRecPPEM"] = getUint16(fp, headOffset + 46)
			self["head"]["fontDirectionHint"] = getInt16(fp, headOffset + 48)
			self["head"]["indexToLocFormat"] = getInt16(fp, headOffset + 50)
			self["head"]["glyphDataFormat"] = getInt16(fp, headOffset + 52)
			
			# maxp
			maxpOffset = self.tableDirectory["maxp"]["offset"]
			self["maxp"] = {}
			self["maxp"]["version"] = getFixed(fp, maxpOffset)
			self["maxp"]["numGlyphs"] = getUint16(fp, maxpOffset + 4)
			self["maxp"]["maxPoints"] = getUint16(fp, maxpOffset + 6)
			self["maxp"]["maxCompositePoints"] = getUint16(fp, maxpOffset + 8)
			self["maxp"]["maxCompositeContours"] = getUint16(fp, maxpOffset + 10)
			self["maxp"]["maxZones"] = getUint16(fp, maxpOffset + 12)
			self["maxp"]["maxTwilightPoints"] = getUint16(fp, maxpOffset + 14)
			self["maxp"]["maxStorage"] = getUint16(fp, maxpOffset + 16)
			self["maxp"]["maxFunctionDefs"] = getUint16(fp, maxpOffset + 18)
			self["maxp"]["maxInstructionDefs"] = getUint16(fp, maxpOffset + 20)
			self["maxp"]["maxStackElements"] = getUint16(fp, maxpOffset + 22)
			self["maxp"]["maxSizeOfInstructions"] = getUint16(fp, maxpOffset + 26)
			self["maxp"]["maxComponentElements"] = getUint16(fp, maxpOffset + 28)
			self["maxp"]["maxComponentDepth"] = getUint16(fp, maxpOffset + 30)
			
			# loca
			locaOffset = self.tableDirectory["loca"]["offset"]
			self.loca = []
			self.locaOffsetSize = []

			locaType = getUint16 if (self["head"]["indexToLocFormat"] == 0) else getUint32
			locaSize = 2 if (self["head"]["indexToLocFormat"] == 0) else 4
			locaRatio = 2 if (self["head"]["indexToLocFormat"] == 0) else 1

			for i in xrange(self["maxp"]["numGlyphs"]):
				self.loca.append(locaType(fp, locaOffset)
						* locaRatio)
				self.locaOffsetSize.append(locaOffset)
				locaOffset += locaSize
				pass
			pass

			# glyf
			glyfOffset = self.tableDirectory["glyf"]["offset"]
			l = len(self.loca)
			self._glyfDataList = {}
			self.glyf = [None] * l
			for i in xrange(l):
				offset = self.tableDirectory["glyf"]["offset"] + self.loca[i]
				if not self._glyfDataList.has_key(offset):
					isNull = (i + 1 < l and self.loca[i] == self.loca[i + 1])
					self._glyfDataList[offset] = TTFGlyf(fp, offset, isNull)
					pass
				self.glyf[i] = self._glyfDataList[offset]
				pass

			cmapOffset = self.tableDirectory["cmap"]["offset"]

			self.cmap = cls()
			self.cmap.version = getUint16(fp, cmapOffset)
			self.cmap.numberSubtables = getUint16(fp, cmapOffset + 2)
			self.cmap.tables = []
			for i in range(self.cmap.numberSubtables):
				table = {}
				table["platformID"] = getUint16(fp, cmapOffset + 8*i + 4)
				table["platformSpecificID"] = getUint16(fp, cmapOffset + 8*i + 6)
				table["offset"] = getUint32(fp, cmapOffset + 8*i + 8)
				table["data"] = TTFCmap(fp, cmapOffset + table["offset"])

				self.cmap.tables.append(table)
				pass

			def getGlyphIndex(ch):
				def getIndex(item):
					return item["data"]._getGlyphIndex(ch)
				return map(getIndex, self.cmap["tables"])

			def getGlyphIndexs():
				def getIndexs():
					return item["data"]._getGlyphIndexs
				return map(getIndex, self.cmap["tables"])

			self.cmap["getGlyphIndex"] = getGlyphIndex
			pass
		pass
	pass

if __name__ == '__main__':
	fontfile = "LLIconfont.ttf"
	ttf = TTF(fontfile)
	ttf.readTables()
	t = ttf.cmap.getGlyphIndex(u'\ue600')

	print(t)


