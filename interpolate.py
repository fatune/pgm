import numpy as np

def interpolate2m(mxx,myy,B):
	# Interpolation from grid to markers p.117 eq.8.19
	i_res, j_res = B.shape

	mxx_int = mxx.astype(int)
	myy_int = myy.astype(int)

	mxx_res = mxx - mxx_int
	myy_res = myy - myy_int
	values = np.zeros(np.shape(mxx_int))
	for idx in range(len(mxx_int)):
		i = myy_int[idx]
		j = mxx_int[idx]
		x = mxx_res[idx]
		y = myy_res[idx]
		if (i > i_res-2) and (j > j_res-2):
			values[idx] = B[i,j]
		elif i > i_res-2:
			values[idx] = (B[i,j]*(1-x) + B[i,j+1]*x)*2
		elif j > j_res-2: 
			values[idx] = (B[i,j]*(1-y) + B[i+1,j]*y)*2
		else:
			values[idx] = B[i,j]*(1-x)*(1-y) + B[i,j+1]*x*(1-y) + B[i+1,j]*(1-x)*y + B[i+1,j+1]*x*y
	return values

def interpolate2m_vect(mxx,myy,B):
	# Interpolation from grid to markers p.117 eq.8.19
	i_res, j_res = B.shape

	mxx_int = mxx.astype(int)
	myy_int = myy.astype(int)
	mxx_res = mxx - mxx_int
	myy_res = myy - myy_int
	values = np.zeros(np.shape(mxx_int))

	i = myy_int
	j = mxx_int
	x = mxx_res
	y = myy_res

	msk_i = i>i_res-2 # mask for i>i_res-1
	msk_j = j>j_res-2 # mask for j>i_res-1
	msk_ij_ = np.logical_and(i>i_res-2, j>j_res-2)
	msk_ij = np.logical_not(np.logical_and(i>i_res-2, j>j_res-2))
	msk_nij = np.logical_not(np.logical_or(msk_i,msk_j))
	msk_i = np.logical_and(msk_i,msk_ij)
	msk_j = np.logical_and(msk_j,msk_ij)

	#values[idx] = B[i,j]
	values[msk_ij_] = B[i[msk_ij_],j[msk_ij_]]

	#values[idx] = (B[i,j]*(1-x) + B[i,j+1]*x)
	values[msk_i] = (B[i[msk_i],j[msk_i]]*(1-x[msk_i]) + B[i[msk_i],j[msk_i]+1]*x[msk_i])

	#values[idx] = (B[i,j]*(1-y) + B[i+1,j]*y)
	values[msk_j] = (B[i[msk_j],j[msk_j]]*(1-y[msk_j]) + B[i[msk_j]+1,j[msk_j]]*y[msk_j])

	#values         = B[i,j]*(1-x)*(1-y) + B[i,j+1]*x*(1-y) + B[i+1,j]*(1-x)*y + B[i+1,j+1]*x*y
	values[msk_nij] = B[i[msk_nij],j[msk_nij]]*(1-x[msk_nij])*(1-y[msk_nij]) +\
	                  B[i[msk_nij],j[msk_nij]+1]*x[msk_nij]*(1-y[msk_nij]) + \
	                  B[i[msk_nij]+1,j[msk_nij]]*(1-x[msk_nij])*y[msk_nij] + \
	                  B[i[msk_nij]+1,j[msk_nij]+1]*x[msk_nij]*y[msk_nij]

	return values

def interpolate(mxx,myy,i_res,j_res, datas):
	# Bilineral interpolation (first-order accurate) p.116 eq.8.18
	mxx_round = np.round(mxx).astype(int)
	myy_round = np.round(myy).astype(int)
	mxx_res = np.abs(mxx - mxx_round)
	myy_res = np.abs(myy - myy_round)
	wm = (1 - mxx_res)*(1-myy_res)

	down = np.zeros((i_res,j_res))
	values = []
	for i in range(len(datas)):
		values.append(np.zeros((i_res,j_res)))
	
	np.add.at(down,(myy_round,mxx_round),wm)

	for i in range(len(values)):
		np.add.at(values[i],(myy_round,mxx_round),wm*datas[i])
		values[i] = values[i]/down
	return values

def interpolate_harmonic(mxx,myy,i_res,j_res,data):
	# Bilineral harmonic interpolation (first-order accurate) p.184 eq.13.10
	mxx_round = np.round(mxx).astype(int)
	myy_round = np.round(myy).astype(int)
	mxx_res = np.abs(mxx - mxx_round)
	myy_res = np.abs(myy - myy_round)
	wm = (1 - mxx_res)*(1-myy_res)
	wm_data = wm/data

	down = np.zeros((i_res,j_res))
	values = np.zeros((i_res,j_res))

	np.add.at(down,(myy_round,mxx_round),wm)
	np.add.at(values,(myy_round,mxx_round),wm_data)

	values = down/values
	return values

def interpolate_single(mxx,myy, i_res,j_res, data):
	# Bilineral interpolation (first-order accurate) p.116 eq.8.18
	mxx_round = np.round(mxx).astype(int)
	myy_round = np.round(myy).astype(int)
	mxx_res = np.abs(mxx - mxx_round)
	myy_res = np.abs(myy - myy_round)
	wm = (1 - mxx_res)*(1-myy_res)
	wm_data = wm * data

	down = np.zeros((i_res,j_res))
	values = np.zeros((i_res,j_res))

	np.add.at(down,(myy_round,mxx_round),wm)
	np.add.at(values,(myy_round,mxx_round),wm_data)

	values = values/down
	return values
